"""

Metadata Navigator
==================
metadatanavigator.py
======

All the logic behind the tool.
The init script will handle config and command line arguments and call the specific functions to configure the tool. 
For both modes (interative/pipe) the init script (mnavigator.py) will call  the function mnavigator. Mnavigator fuction will handle the mode of usage of the tool.  

"""

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
    """
    Sets global configuration from commandline arguments and YAML configfile (mnavigator.py)
    """
    global config
    config=cfg
    if DEBUG:
        print("SETCONFIG:", config)

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
    """
    Display tool help. Usually called after an exception if DEBUG is disable. 
    """
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
    print(colored("Metadata Navigator\n===================", warning, attrs=['bold']))
    print(colored(HELP, detail))

promptstr=str('Metadata Navigator')
colonfill='/'

def get_prompt_tokens(cli):
    """
    Return prompt tokens for custom prompt. 
    """
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
    """
    Return toolbar tokens for custom toolbar. 
    """
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
    """
    Return WordCompleter object to prompt. This will be used to populate the AutoCompletion prompt-toolkit function. 
    """
    return WordCompleter(words, ignore_case=True)

def setwords(content):
    """
    Return two lists. 
    The first list contains all possible inputs to be used by the AutoSuggestion feature of prompt-toolkit. 
    The second list contains all possible metadata input only, without tool comands. This is usefull to send a clean list of possible metadata options to the user when the l|list command is issued.  
    """
    return content+exitkeywords+clikeywords+bkeywords+rkeywords+ckeywords, content

def getmetadata(url=metadataurl):
    """
    Call the metadata api at url and return a list of text results from the request call to the Metadata api. 
    """
    if DEBUG:
        print("GETMETADATA URL:", url)
    try:

        """ This is a hack for a special case of values with an = """
        if "=" in url:
            temp=url.split("/")
            for i, t in enumerate(temp):
                if "=" in t:
                    temp[i]=t.split("=")[0]
            url="/".join(temp)

        req = request("GET",url)
        if not req.ok:
            raise ValueError(req.status_code)
        if DEBUG: 
            print("GETMETADATA: ", req, req.text)
        return req.text.split('\n') 
    except:
        print(colored("404 Not Found - Error\n\n", warning, attrs=['bold']))
        if DEBUG:
            print(logging.exception("Stack:"))
        raise ValueError("404 Not Found")

class SuggestMetadata(AutoSuggest):
    """
    Custom AutoSuggest object used by the prompt-toolkit prompt. Return suggestions based on the current metadata available at the current path and possible tool commands. 
    """
    def __init__(self, words):
        super(SuggestMetadata, self).__init__()
        self.words=words
    def get_suggestion(self, cli, buffer, document):
        for choice in self.words:
            if choice.startswith(document.text.lower()):
                return Suggestion(choice[len(document.text):])

class CompleterAhead(Completer):
    """
    WIP:
        A custom Completer object to be used by the prompt-toolkit. At the moment, I am using the WordCompleter builtin object. The idea here is to find a way to, based on the current input word under cursor, read ahead from the metadata api e return possible "future" inputs. 
    """
    def __init__(self, words, url):
        super(CompleterAhead, self).__init__()
        self.words=words
        self.url=url
    def get_completions(self, document, complete_event):
        currentword = document.get_word_under_cursor()
        if currentword.endswith("/"):
            self.words=(getmetadata(self.url+"/"+currentword))
            print(self.words, type(self.words))
        for choice in self.words:
            if choice.startswith(currentword.lower()):
                yield Completion(choice, -len(currentword))

def getjsonstatus():
    """
    Return global JSON boolean. 
    Enable=True
    Disable=False
    The global variable will determine if the cli output should be formatted in JSON. 
    """
    return JSON

def setjsonstatus():
    """
    Turn JSON output format on/off. 
    """
    global JSON
    if JSON:
        JSON=False
    else:
       JSON=True
    if DEBUG:
        print("SETJSONSTATUS: ", JSON)

def getcolorstatus():
    """
    Return global COLOR boolean. 
    Enable=True
    Disable=False
    This global variable will determine if the cli should be colored. 
    """
    return COLOR

def setcolorstatus():
    """
    Turn colored output format on/off.
    """
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
        print("SETCOLORSTATUS: STATUS, settings", COLOR, common, warning, detail)

def setdebugstatus(onoff=False):
    """
    Turn custom DEBUG mode on/off
    """
    global DEBUG
    if DEBUG:
        print("SETDEBUGSTATUS:", DEBUG)
    DEBUG=onoff

manager = KeyBindingManager.for_prompt()
@manager.registry.add_binding(Keys.ControlT)
def _(event):
    """
    This prompt-toolkit custom KEY binding event for Ctrl+T will turn the JSON output format support on/off calling setjsonstatus() function.
    """
    def setjson():
        if getjsonstatus():
            setjsonstatus()
            print(colored('json mode off',warning))
        else:
            setjsonstatus()
            print(colored('json mode on',warning))
    event.cli.run_in_terminal(setjson)

@manager.registry.add_binding(Keys.ControlY)
def _(event):
    """
    This prompt-toolkit custom KEY binding event for Ctrl+Y will turn the colored output format support on/off calling setjsonstatus() function.
    """
    def setcolor():
        if getcolorstatus():
            setcolorstatus()
            print(colored('color mode off',warning))
        else:
            setcolorstatus()
            print(colored('color mode on',warning))
    event.cli.run_in_terminal(setcolor)

def pipemode(pipemodepath="/"):
    """
    This function will be called by mnavigator when the tool is used with the -p PATH parameter. The function will get the metadata available at PATH and return it directly to the SHELL, based on the output format configured.

    Keywords arguments: 
        pipemodepath -- URL string of the metadata queried. Default = root. 
    """
    global JSON
    global COLOR

    """ This is a hack for a special case of values with an = """
    if "=" in pipemodepath:
        temp=pipemodepath.split("/")
        for i, t in enumerate(temp):
            if "=" in t:
                temp[i]=t.split("=")[0]
        pipemodepath="/".join(temp)

    try:
        words=getmetadata(metadataurl+"/"+pipemodepath)
        if JSON:
            result=json.dumps({pipemodepath: words}, indent=4)
            if COLOR:
                print((highlight(result,JsonLexer(), TerminalFormatter())))
            else:
                print(result)
        else:
            if len(words)>1:
                print(colored(words, detail))
            else:
                print(colored(pipemodepath+":",detail),colored(words.pop(), common))
        return True
    except:
        return False

def recursivemetadata(url, current=[]):

    result=getmetadata(url)
    for i in result:
        if not any(x in i for x in ["/","="]):
            current.append({url:{i:getmetadata(url+"/"+i).pop()}})
            return current
        else:
            return recursivemetadata(url+i,current)

def metadatadump():
    """
    This function will navigate recursively through all metadata. 
    """
    words=[]

    if DEBUG:
        print(words)
        print(path)

    result=getmetadata()
    for i in result:
        if not any(x in i for x in ["/","="]):
            words.append({i:getmetadata(metadataurl+"/"+i).pop()})
        else:
            words.append(recursivemetadata(metadataurl+"/"+i))

    return json.dumps(words,indent=2)


"""    if path:

        try:
            result=getmetadata(metadataurl+"/"+path)
        except ValueError:
            print(colored("Warning: could not fetch metadata "+path, warning))
            return ["ERROR"] 

        for i in result:
            if i.endswith("/"):
#                words[path][i]=metadatadump(words, path+"/"+i)
                  pass
            else:
                words[path][i]=getmetadata(metadataurl+"/"+path+"/"+i).pop()

        return words

    if not path:
        try:
            result=getmetadata()
        except:
            print(colored("Warning: could not fetch metadata "+path, warning))
            return ["ERROR"] 
        for i in result:
            if i.endswith("/"):
                words[i]={}
                words=metadatadump(words, i)
            else:
                words[i]=getmetadata(metadataurl+"/"+i).pop()
        return words
"""

def processUserInput(user_input, meta, w, c):
    """
    This function will process userinput and return words,cleandata and True/False if it was able to proper process the input. 
    """
    global colonfill
    global JSON
    global COLOR

    """ This is a hack for a special case of values with an = """
    if "=" in user_input:
        temp=user_input.split("/")
        for i, t in enumerate(temp):
            if "=" in t:
                temp[i]=t.split("=")[0]
        user_input="/".join(temp)

    try:

       if user_input in set(ckeywords):
           """Just clear the screehn"""
           clear()
           return meta, w, c, True

       elif user_input in set(exitkeywords):
           """Exit tool"""
           exit(0)

       elif user_input in set(bkeywords):
           """Go back one path"""
           head, tail = split(colonfill.rstrip('/'))
           colonfill=head
           meta=metadataurl+"/"+colonfill
           if DEBUG: print("USER_INPUT DEBUG (BACK): ",meta)
           w, c=setwords(getmetadata(meta))
           return meta, w, c, True

       elif user_input in set(rkeywords):
           """Reset metadata path"""
           colonfill="/"
           meta=metadataurl
           if DEBUG: print("USER_INPUT DEBUG (RESET): ",meta)
           w, c = setwords(getmetadata(meta))
           return meta, w, c, True

       elif user_input in set(clikeywords):
           """List current path options"""
           if DEBUG: print("USER_INPUT DEBUG (LIST): ",c)
           if JSON:
               result=json.dumps({'metadata': c}, indent=4)
               if COLOR:
                   print(highlight(result,JsonLexer(), TerminalFormatter()))
               else:
                   print(result)
           else:
               print(colored(c,detail))
           return meta, w, c, True

       elif '/' in user_input:
           """Enter new path"""
           try:
               if not colonfill.endswith("/"): colonfill=colonfill+"/"
               colonfill=colonfill+user_input
               meta=meta+"/"+user_input
               if DEBUG: print("USER_INPUT DEBUG (CATEGORYLIST): ",c)
               w, c= setwords(getmetadata(meta))
               return meta, w, c, True
           except Exception as e:
               print(colored("404 Not Found - Error\n\n", warning, attrs=['bold']))
               if DEBUG:
                   print(logging.exception("Stack:"))
               gethelp()
               return meta, w, c, False

       else:
           """Print metadata value"""
           try:
               result=request("GET",meta+"/"+user_input)
               if not result.ok:
                    raise
               if JSON:
                   filtered=json.dumps({user_input:result.text})
                   if COLOR:
                       print(highlight(filtered, JsonLexer(), TerminalFormatter()))
                   else:
                       print(filtered)
               else:
                   filtered=colored(user_input,detail)+": "+colored(result.text,common)
                   print(filtered)
               if DEBUG: print("USER_INPUT DEBUG (CONTENT): ",filtered)
               return meta, w, c, True
           except Exception as e:
               print(colored("404 Not Found - Error\n\n", warning, attrs=['bold']))
               if DEBUG:
                   print(logging.exception("Stack:"))
               gethelp()
               return meta, w, c, False

    except Exception as e:
        print(colored("Unrecoverable Error", warning, attrs=['bold']))
        if DEBUG: 
            print(colored(logging.exception("Stack:"), 'green'))
            exit(1)

def mnavigator(pipe=False, pipemodepath="/"):
    """
    This function will be called by mnavigator after handling arguments and YAML config setup. 
    If pipe=True, the function will enter the interactive mode in a while loop that will handle user input using a prompt-toolkit configured prompt.
    If pipe=False, the function will enter the "pipe" mode and will call the pipemode function using the pipemodepath as argument.

    Keywords arguments: 
        pipe -- BOOLEAN that will set the tool use mode (INTERACTIVE|PIPE)
        pipemodepath -- URL string of the metadata queried. Default = root. 
    """
    global colonfill
    global JSON
    global COLOR
    meta = metadataurl
    metadatalist = getmetadata(meta)
    words, cleandata = setwords(metadatalist)
    history=InMemoryHistory()
    if pipe:
       piperesult=pipemode(pipemodepath)
       if piperesult:
           exit(0)
       else:
           if DEBUG: raise
           exit(1) 
    gethelp()
    try:
        while True:
            currenturl=meta
            if DEBUG: print("Current URL DEBUG:",meta)
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
            meta, words, cleandata, result=processUserInput(user_input, meta, words, cleandata)

    except Exception as e:
        print(colored("Unrecoverable Error", warning, attrs=['bold']))
        if DEBUG: print(colored(logging.exception("Stack:"), 'green'))
        exit(1)

