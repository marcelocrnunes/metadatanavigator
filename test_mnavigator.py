from mnavigator import create_parser
from argparse import Namespace

import unittest

class MnavigatorTests(unittest.TestCase):

    def test_create_parser(self):
        args=create_parser()
        self.assertIs(type(args),Namespace) 


if __name__ == '__main__': 
    unittest.main()
