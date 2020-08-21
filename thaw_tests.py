import os
import pathlib
import shutil, tempfile
import unittest

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
        
        
    # THIS TEST WAS TO SEE HOW TO SET UP A TEMP DIR & SWITCH TO IT; KEEPING FOR RECORD    
    # def testTempDirectoryFormation(self):
    #     self.setUpTempDirectory()
    #     self.createTempRequirementsDotTxt()
    #     print('test directory should be set up with req file')
    #     print(self.test_dir)
    #     temp_path = self.test_dir
    #     print(f"Temp Path: {temp_path}")
    #     orig_path = os.getcwd()
    #     print(f"This path: {orig_path}")
    #     os.chdir(temp_path)
    #     print(f"now path: {os.getcwd()}")
    #     print(os.listdir(os.getcwd()))
    #     thaw.main()
    #     os.chdir(orig_path)
    #     self.tearDownTempDirectory()
    

    
    # HELPER METHOD TESTS ----------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def testVersionUpdateScaleReturnsMajor(self):
        self.assertEqual(thaw.version_update_scale('1.0','2.1'),"major")
    
    def testVersionUpdateScaleReturnsMinor(self):
        self.assertEqual(thaw.version_update_scale('1.0.0','1.1.6'),"minor")
    
    def testVersionUpdateScaleReturnsMicro(self):
        self.assertEqual(thaw.version_update_scale('1.0.0','1.0.1'),"micro")
    
    def testVersionUpdateScaleReturnsNone(self):
        self.assertEqual(thaw.version_update_scale('1.0','1.0'),None)
    
    # ------------------------------   
    
    def testLibraryInstanceNotSubwordReturnsFalseForSubwordInMiddleOfWord(self):
        self.assertEqual(thaw.library_instance_not_subword('os','the cost is prohibitive'),False)
    
    def testLibraryInstanceNotSubwordReturnsFalseForSubwordAtBeginningOfWord(self):
        self.assertEqual(thaw.library_instance_not_subword('os','the word ossify means to turn into bone'),False)
        
    def testLibraryInstanceNotSubwordReturnsFalseForSubwordAtBeginningOfLine(self):
        self.assertEqual(thaw.library_instance_not_subword('os','ostentatious means very showy'),False)
    
    def testLibraryInstanceNotSubwordReturnsFalseForSubwordAtEndOfWord(self):
        self.assertEqual(thaw.library_instance_not_subword('os','kangaroos are wild animals'),False)
        
    def testLibraryInstanceNotSubwordReturnsFalseForSubwordAtEndOfLine(self):
        self.assertEqual(thaw.library_instance_not_subword('os','we tave two tenors and three sopranos'),False)
    
    def testLibraryInstanceNotSubwordReturnsTrueForNoSubword(self):
        self.assertEqual(thaw.library_instance_not_subword('os','pathname = os.path.dirname("file")'),True)
    
    def testLibraryInstanceNotSubwordRaisesExceptionIfLibraryNameNotInString(self):
        self.assertRaises(thaw.WrongAssumptionError,thaw.library_instance_not_subword,"os","The library should not be found in this line")

    # ------------------------------  
    
    def testCheckLineForNewVariableWithNoVariableButLibraryPresent(self):
        self.assertEqual(thaw.check_line_for_new_variable('dt', 'dt.date.today()'),[])
        
    def testCheckLineForNewVariableShouldThrowErrorIfLibraryNameNotInString(self):
        self.assertRaises(thaw.WrongAssumptionError,thaw.check_line_for_new_variable,'dt','total = price + tax')
        
    def testCheckLineForNewVariableWithVariable(self):
        self.assertEqual(thaw.check_line_for_new_variable('dt','today = dt.date.today()'),['today'])

    
    # PYPI SEARCH METHOD TESTS -----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    
    def testHackyParseForLibraryTitle(self):
        html_str = '''\
        <div class="banner">
            <div class="package-header">
                <div class="package-header__left">
                    <h1 class="package-header__name">
                        numpy 1.19.1
                    </h1>
                    <p class="package-header__pip-instructions">
                        <span id="pip-command">pip install numpy</span>
                        <button type="button" class="copy-tooltip copy-tooltip-s" data-clipboard-target="#pip-command" data-tooltip-label="Copy to clipboard">
                            <i class="fa fa-copy" aria-hidden="true"></i>
                            <span class="sr-only">Copy PIP instructions</span>
                        </button>
                    </p>
                </div>
                <div class="package-header__right">
                    <a class="status-badge status-badge--good" href="/project/numpy/">
                        <span>Latest version</span>
                    </a>
                    <p class="package-header__date">
                        Released: <time datetime="2020-07-21T20:54:49+0000" data-controller="localized-time" data-localized-time-relative="true" data-localized-time-show-time="false" title="2020-07-21 16:54:49" aria-label="2020-07-21 16:54:49">Jul 21, 2020</time>
                    </p>
                </div>
            </div>
        </div>
        '''
        self.assertEqual(thaw.hacky_parse_for_library_title(html_str),'numpy 1.19.1')
    
    
    # PROJECT SEARCH METHOD TESTS --------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    
    def testCheckFileForLibraryNoLibraryPresent(self):
        self.setUpTempDirectory()
        self.createTempDotPyFile('here is some\nmultiline text')
        self.assertEqual(thaw.check_file_for_library(os.path.join(self.test_dir, 'temp.py'),'idna'),[])
        self.tearDownTempDirectory()
    
    def testCheckFileForLibraryImportLibraryButLibraryNameIsInComment(self):
        self.setUpTempDirectory()
        self.createTempDotPyFile('import idna\nx = 3\ny = 4\nz = x + y # this does not actually use the idna library')
        self.assertEqual(thaw.check_file_for_library(os.path.join(self.test_dir, 'temp.py'),'idna'),[])
        self.tearDownTempDirectory()
        
    def testCheckFileForLibraryWhereLibraryNotImportedButNameIsOnlyInComment(self):
        self.setUpTempDirectory()
        self.createTempDotPyFile('x = 3\ny = 4\nz = x + y # this does not actually use OR import the idna library')
        self.assertEqual(thaw.check_file_for_library(os.path.join(self.test_dir, 'temp.py'),'idna'),[])
        self.tearDownTempDirectory()
    
    def testCheckFileForLibraryImportLibrary(self):
        self.setUpTempDirectory()
        self.createTempDotPyFile('import idna #line1\n#line2\nprint idna.decode("xn--eckwd4c7c.xn--zckzah") #line3')
        self.assertEqual(thaw.check_file_for_library(os.path.join(self.test_dir, 'temp.py'),'idna'),[3])
        self.tearDownTempDirectory()
    
    def testCheckFileForLibraryFromLibraryImportOneModule(self):
        text = 'from datetime import date #line1\n#line2\nprint(date.today()) #line3'
        self.setUpTempDirectory()
        self.createTempDotPyFile(text)
        self.assertEqual(thaw.check_file_for_library(os.path.join(self.test_dir, 'temp.py'),'datetime'),[3])
        self.tearDownTempDirectory()
    
    def testCheckFileForLibraryFromLibraryImportTwoModules(self):
        text = 'from datetime import date, time #1\n#2\ntoday = date.today() #3\nepoch = time.time() #4'
        self.setUpTempDirectory()
        self.createTempDotPyFile(text)
        self.assertEqual(thaw.check_file_for_library(os.path.join(self.test_dir, 'temp.py'),'datetime'),[3,4])
        self.tearDownTempDirectory()

    def testCheckFileForLibraryImportLibraryAsAlias(self):
        text = 'import datetime as dt #1\n#2\nelapsed = dt.timedelta(2) #3\nelapsed2 = dt.timedelta(3) #4'
        self.setUpTempDirectory()
        self.createTempDotPyFile(text)
        self.assertEqual(thaw.check_file_for_library(os.path.join(self.test_dir, 'temp.py'),'datetime'),[3,4])
        self.tearDownTempDirectory()
    
    def testCheckFileForLibraryFromLibraryImportOneModuleAsAlias(self):
        text = 'from datetime import date as d #1\n#2\nd.today() #3'
        self.setUpTempDirectory()
        self.createTempDotPyFile(text)
        self.assertEqual(thaw.check_file_for_library(os.path.join(self.test_dir, 'temp.py'),'datetime'),[3])
        self.tearDownTempDirectory()
    
    def testCheckFileForLibraryAndIdentifyVariables(self):
        text = 'import datetime #1\n#2\ndelta = datetime.timedelta(2) #3\n#4\ndelta * 2 #5'
        self.setUpTempDirectory()
        self.createTempDotPyFile(text)
        self.assertEqual(thaw.check_file_for_library(os.path.join(self.test_dir, 'temp.py'),'datetime'),[3,5])
        self.tearDownTempDirectory()

    
if __name__ == '__main__':
    unittest.main()