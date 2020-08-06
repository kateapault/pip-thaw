import shutil, tempfile
import os
import pathlib
import unittest
from urllib import request

from thaw import thaw

class ThawTests(unittest.TestCase):
    # SETUP METHODS ----------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    
    def setUpTempDirectory(self):
        self.test_dir = tempfile.mkdtemp('example')
    
    def createTempRequirementsDotTxt(self):
        f = open(os.path.join(self.test_dir, 'requirements.txt'), 'w')
        # library with major update needed ()
        # f.write('\n')
        # library with minor update needed (2.8 -> 2.10)
        f.write('idna==2.8\n')
        # library with micro update needed (1.19.0 -> 1.19.1)
        # f.write('\n')    
        # library with no update needed
        # f.write('\n')
        # library with no version number included
        # f.write('')
        f.close()
    
    def tearDownTempDirectory(self):
        shutil.rmtree(self.test_dir)
        
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
    
    def testPackageInstanceNotSubwordReturnsFalseForSubwordInMiddleOfWord(self):
        self.assertEqual(thaw.package_instance_not_subword('os','the cost is prohibitive'),False)
    
    def testPackageInstanceNotSubwordReturnsFalseForSubwordAtBeginningOfWord(self):
        self.assertEqual(thaw.package_instance_not_subword('os','the word ossify means to turn into bone'),False)
        
    def testPackageInstanceNotSubwordReturnsFalseForSubwordAtBeginningOfLine(self):
        self.assertEqual(thaw.package_instance_not_subword('os','ostentatious means very showy'),False)
    
    def testPackageInstanceNotSubwordReturnsFalseForSubwordAtEndOfWord(self):
        self.assertEqual(thaw.package_instance_not_subword('os','kangaroos are wild animals'),False)
        
    def testPackageInstanceNotSubwordReturnsFalseForSubwordAtEndOfLine(self):
        self.assertEqual(thaw.package_instance_not_subword('os','we tave two tenors and three sopranos'),False)
    
    def testPackageInstanceNotSubwordReturnsTrueForNoSubword(self):
        self.assertEqual(thaw.package_instance_not_subword('os','pathname = os.path.dirname("file")'),True)
    
    def testPackageInstanceNotSubwordRaisesExceptionIfPackageNameNotInString(self):
        self.assertRaises(thaw.WrongAssumptionError,thaw.package_instance_not_subword,"os","The package should not be found in this line")

    
    # PYPI SEARCH METHOD TESTS -----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    
    def testHackyParseForPackageTitle(self):
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
        self.assertEqual(thaw.hacky_parse_for_package_title(html_str),'numpy 1.19.1')
    
    
    # PROJECT SEARCH METHOD TESTS --------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    
    def testCheckFileForLibraryNoLibraryPresent(self):
        pass
    
    def testCheckFileForLibraryWhereLibraryNameIsInComment(self):
        pass
    
    def testCheckFileForLibraryImportLibrary(self):
        pass
    
    def testCheckFileForLibraryFromLibraryImportOneModule(self):
        pass
    
    def testCheckFileForLibraryFromLibraryImportTwoModules(self):
        pass

    def testCheckFileForLibraryImportLibraryAsAlias(self):
        pass
    
    def testCheckFileForLibraryFromLibraryImportOneModuleAsAlias(self):
        pass
    
    def testCheckFileForLibraryAndIdentifyVariables(self):
        pass
    
    
    # MAIN METHOD TESTS ------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def testShouldThrowExceptionIfRequirementsFileAbsent(self):
        pass
    
    def testThawShouldShowOneMajorUpdate(self):
        pass
    
    def testThawShouldShowOneMinorUpdate(self):
        pass
    
    def testThawShouldShowOneMicroUpdate(self):
        pass
    
    def testThawShouldShowNoUpdates(self):
        pass
    
    def testThawShouldShowOneOfEachUpdateLevel(self):
        pass
    
if __name__ == '__main__':
    unittest.main()