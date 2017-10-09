from mnavigator import create_parser
from metadatanavigator import get_prompt_tokens, get_toolbar_tokens
from prompt_toolkit.token import Token
from argparse import Namespace

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

if __name__ == '__main__': 
    unittest.main()
