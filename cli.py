from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import Suggestion, AutoSuggest
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from os.path import split
from requests import request
from termcolor import colored
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from sys import exit

import json
import logging

metadataurl="http://169.254.169.254/latest/meta-data/"

config={'jsonenable': False, 'toolbarcolor': '#ansiblack bg:#ansiwhite', 'promptcolor': {'text': '#ansidarkgray bold', 'prompt': '#ansiblue bold'}, 'color': {'warning': 'red', 'detail': 'green', 'common': 'white'}, 'debug': False, 'colorenable': False}

def setconfig(cfg):
    global config
    config=cfg
    if DEBUG:
        print "SETCONFIG:", config

DEBUG = config['debug']
JSON = config['jsonenable']
COLOR = config['colorenable']

style = style_from_dict({
    Token.Text: config['promptcolor']['text'],
    Token.Colon: config['promptcolor']['prompt'],
    Token.Color: config['toolbarcolor']+' bold',
    Token.Json: config['toolbarcolor']+' bold',
    Token.Toolbar: config['toolbarcolor'],
    Token.ColorR: config['toolbarcolor']+' bold reverse',
    Token.JsonR: config['toolbarcolor']+' bold reverse',
    Token.TextNoColor: '#ansiwhite bold',
    Token.ColonNoColor: '#ansiwhite bold'

})

exitkeywords=["q","quit"]
clikeywords=["l","list",""]
bkeywords=["b","back"]
rkeywords=["r","reset"]
ckeywords=["c","clear"]


common=config['color']['common']

if COLOR:
    detail=config['color']['detail']
    warning=config['color']['warning']
else:
    detail=common
    warning=common

def gethelp():
    HELP= """
INTERATIVE MODE:
Press ENTER, l, or list to view available metadata options.
Enter metadata name to view it's current value.
Enter path name with trailling slash to navigate further on the categories
Enter "b" or "back" to go back to previous metadata category
Enter "r" or "reset" to go to root path
Enter "c" or "clear" to clear the screen
Enter "q" or "quit" to quit.
Press "Ctrl-t" to toggle json mode (-j option on the commandline)
Press "Ctrl-y" to toggle color mode (-c option on the commandline)

PIPE MODE:
Call the command with the "-p" argument. Call the command with "-h" for usage help.

    """
    print colored("Metadata Navigator\n===================", warning, attrs=['bold'])
    print colored(HELP, detail)

promptstr=unicode('Metadata Navigator')
colonfill='/'

def get_prompt_tokens(cli):
    if COLOR:
        return [
        (Token.Text, promptstr),
        (Token.Colon, '['+colonfill+']> '),
        ]
    else:
        return [
        (Token.TextNoColor, promptstr),
        (Token.ColonNoColor, '['+colonfill+']> '),
        ]

def get_toolbar_tokens(cli):
    toolbarlist=[(Token.Toolbar,"")]
    if COLOR:
        toolbarlist.append((Token.Color,"[color] "))
    else:
        toolbarlist.append((Token.ColorR,"[color] "))
    if JSON:
        toolbarlist.append((Token.Json,"[json] "))
    else:
        toolbarlist.append((Token.JsonR,"[json] "))
    return toolbarlist

def setcompleter(words):
    return WordCompleter(words, ignore_case=True)

def setwords(content):
    return content+exitkeywords+clikeywords+bkeywords+rkeywords+ckeywords, content

def getmetadata(url):
    try:
        req = request("GET",url)
        if not req.ok:
            raise
        if DEBUG: 
            print "GETMETADATA: ", req
        return req.content.split('\n')
    except:
        print colored("404 Not Found - Error\n\n", warning, attrs=['bold'])
        gethelp()
        return []

class SuggestMetadata(AutoSuggest):
    def __init__(self, words):
        super(SuggestMetadata, self).__init__()
        self.words=words
    def get_suggestion(self, cli, buffer, document):
        for choice in self.words:
            if choice.startswith(document.text.lower()):
                return Suggestion(choice[len(document.text):])

class CompleterAhead(Completer):
    def __init__(self, words, url):
        super(CompleterAhead, self).__init__()
        self.words=words
        self.url=url
    def get_completions(self, document, complete_event):
        currentword = document.get_word_under_cursor()
        if currentword.endswith("/"):
            self.words=(getmetadata(self.url+"/"+currentword))
            print self.words, type(self.words)
        for choice in self.words:
            if choice.startswith(currentword.lower()):
                yield Completion(choice, -len(currentword))

def getjsonstatus():
    return JSON

def setjsonstatus():
    global JSON
    if JSON:
        JSON=False
    else:
       JSON=True
    if DEBUG:
        print "SETJSONSTATUS: ", JSON

def getcolorstatus():
    return COLOR

def setcolorstatus():
    global COLOR
    global warning, common, detail, config
    if COLOR:
        COLOR=False
        common=config['color']['common']
        warning=common
        detail=common
    else:
       COLOR=True
       warning=config['color']['warning']
       detail=config['color']['detail']
    if DEBUG:
        print "SETCOLORSTATUS: STATUS, settings", COLOR, common, warning, detail

def setdebugstatus(onoff=False):
    global DEBUG
    if DEBUG:
        print "SETDEBUGSTATUS:", DEBUG
    DEBUG=onoff

manager = KeyBindingManager.for_prompt()
@manager.registry.add_binding(Keys.ControlT)
def _(event):
    def setjson():
        if getjsonstatus():
            setjsonstatus()
            print colored('json mode off',warning)
        else:
            setjsonstatus()
            print colored('json mode on',warning)
    event.cli.run_in_terminal(setjson)

@manager.registry.add_binding(Keys.ControlY)
def _(event):
    def setcolor():
        if getcolorstatus():
            setcolorstatus()
            print colored('color mode off',warning)
        else:
            setcolorstatus()
            print colored('color mode on',warning)
    event.cli.run_in_terminal(setcolor)

def pipemode(pipemodepath="/"):
    global JSON
    global COLOR
    words=getmetadata(metadataurl+"/"+pipemodepath)
    if JSON:
        result=json.dumps({pipemodepath: words}, indent=4)
        if COLOR:
            print (highlight(result,JsonLexer(), TerminalFormatter()))
        else:
            print result
    else:
        if len(words)>1:
            print colored(words, detail)
        else:
            print colored(pipemodepath+":",detail),colored(words.pop(), common)

def climode(pipe=False, pipemodepath="/"):
    global colonfill
    global JSON
    global COLOR
    meta = metadataurl
    metadatalist = getmetadata(meta)
    words, cleandata = setwords(metadatalist)
    history=InMemoryHistory()
    if pipe:
       pipemode(pipemodepath)
       exit()
    gethelp()
    try:
        while True:
            currenturl=meta
            if DEBUG: print "Current URL:",meta
            try:
                user_input = prompt(get_prompt_tokens=get_prompt_tokens,
                                style=style,
                                history=history,
                                auto_suggest=SuggestMetadata(words),
                                completer=setcompleter(words),
                                #completer=CompleterAhead(cleandata, currenturl),
                                #complete_while_typing=False,
                                display_completions_in_columns=True,
                                get_bottom_toolbar_tokens=get_toolbar_tokens,
                                key_bindings_registry=manager.registry
                                )
            except KeyboardInterrupt:
                exit(0)
            if user_input in set(ckeywords):
                clear()
            elif user_input in set(exitkeywords):
                exit(0)
            elif user_input in set(bkeywords):
                head, tail = split(colonfill.rstrip('/'))
                colonfill=head
                meta=metadataurl+"/"+colonfill
                if DEBUG: print "USER_INPUT DEBUG: ",meta
                words, cleandata=setwords(getmetadata(meta))
            elif user_input in set(rkeywords):
                colonfill="/"
                meta=metadataurl
                words, cleandata=setwords(getmetadata(meta))
            elif user_input in set(clikeywords):
                if DEBUG: print("WORDS TYPE: %s",type(cleandata))
                if JSON:
                    result=json.dumps({'metadata': cleandata}, indent=4)
                    if COLOR:
                        print (highlight(result,JsonLexer(), TerminalFormatter()))
                    else:
                        print result
                else:
                    print colored(cleandata,detail)
            elif '/' in user_input:
               if not colonfill.endswith("/"): colonfill=colonfill+"/"
               colonfill=colonfill+user_input
               meta=meta+"/"+user_input
               if DEBUG: print meta
               words, cleandata= setwords(getmetadata(meta))
            else:
               try:
                   result=request("GET",meta+"/"+user_input)
                   if not result.ok:
                        raise
                   if JSON:
                       filtered=json.dumps({user_input:result.content})
                       if COLOR:
                           print(highlight(filtered, JsonLexer(), TerminalFormatter()))
                       else:
                           print filtered
                   else:
                       filtered=colored(user_input,detail)+": "+colored(result.content,common)
                       print filtered
               except:
                   print colored("404 Not Found - Error\n\n", warning, attrs=['bold'])
                   gethelp()
    except Exception as e:
        print colored("Unrecoverable Error", warning, attrs=['bold'])
        if DEBUG: print colored(logging.exception("Stack:"), 'green')

