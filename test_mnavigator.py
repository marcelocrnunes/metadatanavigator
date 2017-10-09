from mnavigator import create_parser
from metadatanavigator import get_prompt_tokens, get_toolbar_tokens, setcompleter, setwords, getmetadata, getjsonstatus, setjsonstatus, getcolorstatus, setcolorstatus
from prompt_toolkit.token import Token
from argparse import Namespace
from prompt_toolkit.contrib.completers import WordCompleter


import unittest

class MnavigatorTests(unittest.TestCase):

    def test_create_parser(self):
        result=create_parser()
        self.assertIs(type(result),Namespace) 

    def test_get_prompt_tokens(self):
        result=get_prompt_tokens(None)
        self.assertIs(type(result),list) 
        for i in result: 
            self.assertIs(i[0].parent, Token)

    def test_get_toolbar_tokens(self):
        result=get_toolbar_tokens(None)
        self.assertIs(type(result),list)
        for i in result: 
            self.assertIs(i[0].parent, Token)

    def test_setcompleter(self):
        result=setcompleter(["list"])
        self.assertIs(type(result), WordCompleter)

    def test_setwords(self): 
        result1, result2 = setwords(["list"])
        self.assertIs(type(result1), list)
        self.assertIs(type(result2), list)
        for i in result1: 
            self.assertIs(type(i), str)
        for i in result2:
            self.assertIs(type(i), str)


    def test_getmetadata(self): 
        result=getmetadata() 
        self.assertIs(type(result), list)
        for i in result:
            self.assertIs(type(i), str)
        result=getmetadata("http://169.254.169.254/latest/meta-data/instance-id")
        self.assertIs(type(result), list)
        for i in result:
            self.assertIs(type(i), str)

    def test_getjsonstatus(self):
        result=getjsonstatus()
        self.assertIs(type(result), bool)

    def test_getcolorstatus(self):
        result=getcolorstatus()
        self.assertIs(type(result), bool)

    def test_setjsonstatus(self):
        result=getjsonstatus()
        setjsonstatus()
        result2=getjsonstatus()
        self.assertNotEqual(result,result2)

    def test_setcolorstatus(self):
        result=getcolorstatus()
        setcolorstatus()
        result2=getcolorstatus()
        self.assertNotEqual(result,result2)

if __name__ == '__main__':
    unittest.main(verbosity=2)
