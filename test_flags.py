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
            text = 'import pandas as pd\n\ndf = pd.DataFrame({"Age": [22, 35, 58],"Sex": ["male", "male", "female"]})\nprint(df)'
            self.createTempDotPyFile(text)
        elif label == 'minor': # library with minor update needed (1.0.5 -> 1.1.0)
            f.write('pandas==1.0.5\n')
            text = 'import pandas as pd\n\ndf = pd.DataFrame({"Age": [22, 35, 58],"Sex": ["male", "male", "female"]})\nprint(df)'
            self.createTempDotPyFile(text)
        elif label == 'micro': # library with micro update needed (1.19.0 -> 1.19.1)
            f.write('numpy==1.19.0\n')
            text = 'import numpy as np\n\na = np.arange(15).reshape(3, 5)\nprint(a)'
            self.createTempDotPyFile(text)    
        elif label == 'all': # libraries with major, minor, and micro updates needed
            f.write('idna==2.9\nnumpy==1.19.0\npandas==0.25.3\n')
            text_minor = 'import idna\n\nencoded = idna.encode("ドメイン.テスト")\nprint(idna.decode(encoded))'
            self.createTempDotPyFile(text_minor,'minor')
            text_micro = 'import pandas as pd\n\ndf = pd.DataFrame({"Age": [22, 35, 58],"Sex": ["male", "male", "female"]})\nprint(df)'
            self.createTempDotPyFile(text_micro,'micro')
            text_major = 'import numpy as np\n\na = np.arange(15).reshape(3, 5)\nprint(a)'
            self.createTempDotPyFile(text_major,'major')
        elif label == 'none': # all libraries up to date
            f.write('pandas==1.1.0\n')
            text = 'import pandas as pd\n\ndf = pd.DataFrame({"Age": [22, 35, 58],"Sex": ["male", "male", "female"]})\nprint(df)'
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
    def testFlagOutWithFlagPresent(self):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('all')
        @mock.patch('argparse.ArgumentParser.parse_args',
                    return_value=argparse.Namespace(directory=self.test_dir,out=os.getcwd(),verbose=False,library=None,imports=False))
        def runThawWithMockArgs(mock_args):
            with mock.patch('sys.stdout',new = StringIO()) as mock_out:
                thaw.main()
        
        runThawWithMockArgs()
        thaw_report_file_exists = False
        for file in os.listdir(os.getcwd()):
            if fnmatch.fnmatch(file, 'thaw_report*.txt'):
                thaw_report_file_exists = True
                os.remove(file)
        self.assertTrue(thaw_report_file_exists)
        self.tearDownTempDirectory()
        
    def testFlagOutWithFlagAbsent(self):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('all')
        self.createTempDotPyFile('imports idna #line1\n#line2\nprint idna.decode("xn--eckwd4c7c.xn--zckzah") #line3')
        @mock.patch('argparse.ArgumentParser.parse_args',
                    return_value=argparse.Namespace(directory=self.test_dir,out=None,verbose=False,library=None,imports=False))    
        def runThawWithMockArgs(mock_args):
            with mock.patch('sys.stdout',new = StringIO()) as mock_out:
                thaw.main()
            
        thaw_report_file_exists = False
        for file in os.listdir(self.test_dir):
            if fnmatch.fnmatch(file, 'thaw_report*.txt'):
                thaw_report_file_exists = True
                os.remove(file)
        self.assertFalse(thaw_report_file_exists)
        self.tearDownTempDirectory()

    def testFlagVerboseWithFlagPresent(self):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('major')
        @mock.patch('argparse.ArgumentParser.parse_args',
                    return_value=argparse.Namespace(directory=self.test_dir,out=None,verbose=True,library=None,imports=False))
        def runThawWithMockArgs(mock_args):
            line_text = 'print(df)'
            with mock.patch('sys.stdout',new = StringIO()) as mock_out:
                thaw.main()
                self.assertTrue(1==1)
                self.assertTrue(line_text in mock_out.getvalue())
        runThawWithMockArgs()
        self.tearDownTempDirectory()
        
    
    def testFlagVerboseWithFlagAbsent(self):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('major')
        @mock.patch('argparse.ArgumentParser.parse_args',
                    return_value=argparse.Namespace(directory=self.test_dir,out=None,verbose=False,library=None,imports=False))
        def runThawWithMockArgs(mock_args):
            line_text = 'print(df)'
            with mock.patch('sys.stdout',new = StringIO()) as mock_out:
                self.runThawInTempDirectoryAndReturn()
                self.assertFalse(line_text in mock_out.getvalue())
        runThawWithMockArgs()
        self.tearDownTempDirectory()
        
    def testFlagLibraryWithFlagPresentAndOneLibrary(self):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('all')
        @mock.patch('argparse.ArgumentParser.parse_args',
                    return_value=argparse.Namespace(directory=self.test_dir,out=None,verbose=False,library=['idna'],imports=False))
        def runThawWithMockArgs(mock_args):
            with mock.patch('sys.stdout',new=StringIO()) as mock_out:
                self.runThawInTempDirectoryAndReturn()
                report = mock_out.getvalue()
                self.assertTrue('pandas' not in report and 'numpy' not in report and 'idna' in report)
        runThawWithMockArgs()
        self.tearDownTempDirectory()
    
    def testFlagLibraryWithFlagPresentAndTwoLibraries(self):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('all')
        @mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(directory=self.test_dir,out=None,verbose=False,library=['idna', 'numpy'],imports=False))
        def runThawWithMockArgs(mock_args):
            with mock.patch('sys.stdout',new=StringIO()) as mock_out:
                self.runThawInTempDirectoryAndReturn()
                report = mock_out.getvalue()
                self.assertTrue('pandas' not in report and 'numpy' in report and 'idna' in report)
        runThawWithMockArgs()
        self.tearDownTempDirectory()
    
    def testFlagLibraryWithFlagAbsent(self):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('all')
        @mock.patch('argparse.ArgumentParser.parse_args',
                    return_value=argparse.Namespace(directory=self.test_dir,out=None,verbose=False,library=None,imports=False))
        def runThawWithMockArgs(mock_args):        
            with mock.patch('sys.stdout',new=StringIO()) as mock_out:
                thaw.main()
                report = mock_out.getvalue()
                self.assertTrue('pandas' in report and 'numpy' in report and 'idna' in report)
        runThawWithMockArgs()
        self.tearDownTempDirectory()
        
    def testFlagImportsWithFlagPresent(self):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('all')
        os.remove(os.path.join(self.test_dir,'requirements.txt'))
        @mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(directory=self.test_dir,out=None,verbose=False,library=None,imports=True))
        def runThawWithMockArgs(mock_args):
            with mock.patch('sys.stdout',new=StringIO()) as mock_out:
                thaw.main()
                report = mock_out.getvalue()
                self.assertTrue('pandas' in report and 'numpy' in report and 'idna' in report)
        runThawWithMockArgs()
        self.tearDownTempDirectory()

        
    def testFlagImportsWithFlagAbsent(self):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('all')
        os.remove(os.path.join(self.test_dir,'requirements.txt'))
        @mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(directory=self.test_dir,out=None,verbose=False,library=None,imports=False))
        def runThawWithMockArgs(mock_out):
            with mock.patch('sys.stdout',new=StringIO()) as mock_out:
                thaw.main()
                report = mock_out.getvalue()
                self.assertEqual(report.strip(),"No requirements file found - please run thaw in the top level of your project")
        runThawWithMockArgs()
        self.tearDownTempDirectory()
        
    def testIncompatibleFlagsImportsAndLibrary(self):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('minor')
        @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(directory=self.test_dir,out=None,verbose=False,library=['numpy'],imports=True))        
        def runThawWithMockArgs(mock_args):
            with mock.patch('sys.stdout',new=StringIO()) as mock_out:
                thaw.main()
                report = mock_out.getvalue()
                self.assertEqual(report.strip(),"--library and --imports flags cannot be used in the same report. Instead, please run thaw with one flag and then rerun with the other.")
        runThawWithMockArgs()
        self.tearDownTempDirectory
    
    def testIfMockParamsCanBePassedWithinTest(self):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('all')
        @mock.patch('argparse.ArgumentParser.parse_args',
                    return_value=argparse.Namespace(directory=self.test_dir,out=None,verbose=False,library=['numpy'],imports=False))
        def runningThaw(mock_args):
            with mock.patch('sys.stdout',new=StringIO()) as mock_out:
                thaw.main()
                report = mock_out.getvalue()
                self.assertTrue('pandas' not in report and 'numpy' in report and 'idna' not in report)
        runningThaw()
        self.tearDownTempDirectory()
        
        
    def testDirectorySameAsRunLocation(self):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('all')
        @mock.patch('argparse.ArgumentParser.parse_args',
                    return_value=argparse.Namespace(directory='.',out=None,verbose=False,library=['numpy'],imports=False))
        def runningThaw(mock_args):
            with mock.patch('sys.stdout',new=StringIO()) as mock_out:
                self.runThawInTempDirectoryAndReturn()
                report = mock_out.getvalue()
                self.assertTrue('pandas' not in report and 'numpy' in report and 'idna' not in report)
        runningThaw()
        self.tearDownTempDirectory()
    
    def testDirectoryDifferentThanRunLocation(self):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt('all')
        @mock.patch('argparse.ArgumentParser.parse_args',
                    return_value=argparse.Namespace(directory=self.test_dir,out=None,verbose=False,library=['numpy'],imports=False))
        def runningThaw(mock_args):
            with mock.patch('sys.stdout',new=StringIO()) as mock_out:
                thaw.main()
                report = mock_out.getvalue()
                self.assertTrue('pandas' not in report and 'numpy' in report and 'idna' not in report)
        runningThaw()
        self.tearDownTempDirectory()
    

if __name__ == '__main__':
    unittest.main()