from mnavigator import create_parser
from metadatanavigator import get_prompt_tokens, get_toolbar_tokens, setcompleter, setwords, getmetadata, getjsonstatus, setjsonstatus, getcolorstatus, setcolorstatus, processUserInput, pipemode, mnavigator
from prompt_toolkit.token import Token
from argparse import Namespace
from prompt_toolkit.contrib.completers import WordCompleter


import unittest

class MyNavigatorClear(unittest.TestCase):
    def test_clearthingsup(self):
        try: 
            meta="http://169.254.169.254/latest/meta-data/"
            w=[]
            c=[]
            result=False
            meta, w, c, result=processUserInput("clear",meta,w,c)
            self.assertNotEqual(result, False)
            print("test_clearthingsup ... ok")
        except Exception as e:
            print("Clear test failed")
            raise e

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
        try:
            result=getmetadata("thisShouldNotExistNever")
            self.assertEqual(result, False)
        except:
            pass

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

    def test_processUserInput_back(self):
        meta="http://169.254.169.254/latest/meta-data/network/"
        w=[]
        c=[]
        result=False
        meta, w, c, result=processUserInput("back",meta,w,c)
        self.assertNotEqual(result, False)
        self.assertNotIn("network/",meta)

    def test_processUserInput_reset(self):
        meta="http://169.254.169.254/latest/meta-data/network/interfaces/macs/"
        w=[]
        c=[]
        result=False
        meta, w, c, result=processUserInput("reset",meta,w,c)
        self.assertNotEqual(result, False)
        self.assertEqual(meta,"http://169.254.169.254/latest/meta-data/")

    def test_processUserInput_list(self):
        meta="http://169.254.169.254/latest/meta-data/network/"
        w, c=setwords(getmetadata(meta))
        result=False
        meta, wresult, cresult, result=processUserInput("list",meta,w,c)
        self.assertNotEqual(result, False)
        self.assertEqual(c,cresult)
        self.assertEqual(w,wresult)

    def test_processUserInput_enternewpath(self):
        meta="http://169.254.169.254/latest/meta-data/"
        w, c=setwords(getmetadata(meta))
        metaresult="http://169.254.169.254/latest/meta-data/network/"
        wcheck, ccheck=setwords(getmetadata(metaresult))
        result=False
        meta, wresult, cresult, result=processUserInput("network/",meta,w,c)
        self.assertNotEqual(result, False)
        self.assertEqual(ccheck,cresult)
        self.assertEqual(wcheck,wresult)
        meta="http://169.254.169.254/latest/meta-data/"
        w, c=setwords(getmetadata(meta))
        metaresult, wresult,cresult, result=processUserInput("ThisShouldNeverExist/", meta, w, c)
        self.assertEqual(w, wresult)
        self.assertEqual(c, cresult)
        self.assertEqual(result, False)


    def test_processUserInput_enterinput(self):
        meta="http://169.254.169.254/latest/meta-data/ami-id"
        w, c=setwords(getmetadata(meta))
        result=False
        meta, wresult, cresult, result=processUserInput("ami-id",meta,w,c)
        self.assertNotEqual(result, False)
        self.assertEqual(c,cresult)

    def test_pipemode(self):
        meta="ami-id"
        result=False
        result=pipemode(pipemodepath=meta)
        self.assertNotEqual(result, False)
        meta="ThisShouldNeverExist"
        result=True
        result=pipemode(pipemodepath=meta)
        self.assertNotEqual(result, True)
        meta="network/"
        result=False
        result=pipemode(pipemodepath=meta)
        self.assertNotEqual(result, False)

    def test_callpipemode(self):
        with self.assertRaises(SystemExit) as cm:
            result=mnavigator(True)
        self.assertEqual(cm.exception.code, 0)
        with self.assertRaises(SystemExit) as cm:
            result=mnavigator(True, "Lilico/")
        self.assertEqual(cm.exception.code, 1)
        with self.assertRaises(SystemExit) as cm:
            result=mnavigator(True, "network/")
        self.assertEqual(cm.exception.code, 0)



if __name__ == '__main__':
    #unittest.main(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(MyNavigatorClear)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(MnavigatorTests)
    unittest.TextTestRunner(verbosity=2, buffer=True).run(suite)
