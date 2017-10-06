from mnavigator import create_parser
from unittest import TestCase

class CLITestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        parser = create_parser()
        cls.parser = parser

class mnavigatorTestCase(CLITestCase):
    def test_with_empty_args():
        self.parser.parse_args([])
