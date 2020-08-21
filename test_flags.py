import argparse
import fnmatch
from io import StringIO
import os
import pathlib
import shutil, tempfile
import unittest
from unittest import mock

from src import thaw

class ThawTests(unittest.TestCase):
    # SETUP METHODS ----------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    
    def setUpTempDirectory(self):
        self.test_dir = tempfile.mkdtemp('example')
        
    def createTempDotPyFile(self,text,name='temp'):
        f = open(os.path.join(self.test_dir, f"{name}.py"), 'w')
        f.write(text)
        f.close()
    
    def createTempRequirementsDotTxt(self,label):
        f = open(os.path.join(self.test_dir, 'requirements.txt'), 'w')
        if label == 'major': # library with major update needed (0.25.3 -> 1.1.0)
            f.write('pandas==0.25.3\n')
            text = 'imports pandas as pd\n\ndf = pd.DataFrame({"Age": [22, 35, 58],"Sex": ["male", "male", "female"]})\nprint(df)'
            self.createTempDotPyFile(text)
        elif label == 'minor': # library with minor update needed (1.0.5 -> 1.1.0)
            f.write('pandas==1.0.5\n')
            text = 'imports pandas as pd\n\ndf = pd.DataFrame({"Age": [22, 35, 58],"Sex": ["male", "male", "female"]})\nprint(df)'
            self.createTempDotPyFile(text)
        elif label == 'micro': # library with micro update needed (1.19.0 -> 1.19.1)
            f.write('numpy==1.19.0\n')
            text = 'imports numpy as np\n\na = np.arange(15).reshape(3, 5)\nprint(a)'
            self.createTempDotPyFile(text)    
        elif label == 'all': # libraries with major, minor, and micro updates needed
            f.write('idna==2.9\nnumpy==1.19.0\npandas==0.25.3\n')
            text_minor = 'imports idna\n\nencoded = idna.encode("ドメイン.テスト")\nprint(idna.decode(encoded))'
            self.createTempDotPyFile(text_minor,'minor')
            text_micro = 'imports pandas as pd\n\ndf = pd.DataFrame({"Age": [22, 35, 58],"Sex": ["male", "male", "female"]})\nprint(df)'
            self.createTempDotPyFile(text_micro,'micro')
            text_major = 'imports numpy as np\n\na = np.arange(15).reshape(3, 5)\nprint(a)'
            self.createTempDotPyFile(text_major,'major')
        elif label == 'none': # all libraries up to date
            f.write('pandas==1.1.0\n')
            text = 'imports pandas as pd\n\ndf = pd.DataFrame({"Age": [22, 35, 58],"Sex": ["male", "male", "female"]})\nprint(df)'
            self.createTempDotPyFile(text)
        f.close()
    
    def tearDownTempDirectory(self):
        shutil.rmtree(self.test_dir)
        
    def runThawInTempDirectoryAndReturn(self):
        temp_path = self.test_dir
        orig_path = os.getcwd()
        os.chdir(temp_path)
        thaw.main()
        os.chdir(orig_path)    
    
    
    # FLAG TESTS -------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(out=os.getcwd(),verbose=False,library=None,imports=False))
    def testFlagOutWithFlagPresent(self,mock_args):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('all')
        self.createTempDotPyFile('imports idna #line1\n#line2\nprint idna.decode("xn--eckwd4c7c.xn--zckzah") #line3')
        with mock.patch('sys.stdout',new = StringIO()) as mock_out:
            self.runThawInTempDirectoryAndReturn()
            
        thaw_report_file_exists = False
        for file in os.listdir(os.getcwd()):
            if fnmatch.fnmatch(file, 'thaw_report*.txt'):
                thaw_report_file_exists = True
                os.remove(file)
        self.assertTrue(thaw_report_file_exists)
        self.tearDownTempDirectory()
        
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(out=None,verbose=False,library=None,imports=False))    
    def testFlagOutWithFlagAbsent(self,mock_args):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('all')
        self.createTempDotPyFile('imports idna #line1\n#line2\nprint idna.decode("xn--eckwd4c7c.xn--zckzah") #line3')
        with mock.patch('sys.stdout',new = StringIO()) as mock_out:
            self.runThawInTempDirectoryAndReturn()
            
        thaw_report_file_exists = False
        for file in os.listdir(self.test_dir):
            if fnmatch.fnmatch(file, 'thaw_report*.txt'):
                thaw_report_file_exists = True
                os.remove(file)
        self.assertFalse(thaw_report_file_exists)
        self.tearDownTempDirectory()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(out=None,verbose=True,library=None,imports=False))
    def testFlagVerboseWithFlagPresent(self,mock_args):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('major')
        line_text = 'print(df)'
        with mock.patch('sys.stdout',new = StringIO()) as mock_out:
            self.runThawInTempDirectoryAndReturn()
            self.assertTrue(line_text in mock_out.getvalue())
        self.tearDownTempDirectory()
        
    
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(out=None,verbose=False,library=None,imports=False))
    def testFlagVerboseWithFlagAbsent(self,mock_args):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('major')
        line_text = 'print(df)'
        with mock.patch('sys.stdout',new = StringIO()) as mock_out:
            self.runThawInTempDirectoryAndReturn()
            self.assertFalse(line_text in mock_out.getvalue())
        self.tearDownTempDirectory()
        
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(out=None,verbose=False,library=['idna'],imports=False))
    def testFlagLibraryWithFlagPresentAndOneLibrary(self,mock_args):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('all')
        with mock.patch('sys.stdout',new=StringIO()) as mock_out:
            self.runThawInTempDirectoryAndReturn()
            report = mock_out.getvalue()
            self.assertTrue('pandas' not in report and 'numpy' not in report and 'idna' in report)
        self.tearDownTempDirectory()
    
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(out=None,verbose=False,library=['idna', 'numpy'],imports=False))
    def testFlagLibraryWithFlagPresentAndTwoLibraries(self,mock_args):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('all')
        with mock.patch('sys.stdout',new=StringIO()) as mock_out:
            self.runThawInTempDirectoryAndReturn()
            report = mock_out.getvalue()
            self.assertTrue('pandas' not in report and 'numpy' in report and 'idna' in report)
        self.tearDownTempDirectory()
    
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(out=None,verbose=False,library=None,imports=False))
    def testFlagLibraryWithFlagAbsent(self,mock_args):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('all')
        with mock.patch('sys.stdout',new=StringIO()) as mock_out:
            self.runThawInTempDirectoryAndReturn()
            report = mock_out.getvalue()
            self.assertTrue('pandas' in report and 'numpy' in report and 'idna' in report)
        self.tearDownTempDirectory()
        
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(out=None,verbose=False,library=None,imports=True))
    def testFlagImportsWithFlagPresent(self,mock_args):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('all')
        os.remove(os.path.join(self.test_dir,'requirements.txt'))
        r = None
        with mock.patch('sys.stdout',new=StringIO()) as mock_out:
            self.runThawInTempDirectoryAndReturn()
            report = mock_out.getvalue()
            self.assertTrue('pandas' in report and 'numpy' in report and 'idna' in report)
            r = report
            # self.assertTrue(len(report)>0)
        # print(r)
        self.tearDownTempDirectory()

        
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(out=None,verbose=False,library=None,imports=False))
    def testFlagImportsWithFlagAbsent(self,mock_args):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('all')
        os.remove(os.path.join(self.test_dir,'requirements.txt'))
        with mock.patch('sys.stdout',new=StringIO()) as mock_out:
            self.runThawInTempDirectoryAndReturn()
            report = mock_out.getvalue()
            self.assertEqual(report.strip(),"No requirements file found - please run thaw in the top level of your project")
        self.tearDownTempDirectory()
        
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(out=None,verbose=False,library=['numpy'],imports=True))        
    def testIncompatibleFlagsImportsAndLibrary(self,mock_args):
        with mock.patch('sys.stdout',new=StringIO()) as mock_out:
            self.setUpTempDirectory()
            self.createTempRequirementsDotTxt('minor')
            self.runThawInTempDirectoryAndReturn()
            report = mock_out.getvalue()
            self.assertEqual(report.strip(),"--library and --imports flags cannot be used in the same report. Instead, please run thaw with one flag and then rerun with the other.")


    

if __name__ == '__main__':
    unittest.main()