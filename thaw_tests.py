import shutil, tempfile
import os
import pathlib
import unittest

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
        
    
    def testTempDirectoryFormation(self):
        self.setUpTempDirectory()
        self.createTempRequirementsDotTxt()
        print('test directory should be set up with req file')
        print(self.test_dir)
        temp_path = self.test_dir
        print(f"Temp Path: {temp_path}")
        orig_path = os.getcwd()
        print(f"This path: {orig_path}")
        os.chdir(temp_path)
        print(f"now path: {os.getcwd()}")
        print(os.listdir(os.getcwd()))
        thaw.main()
        os.chdir(orig_path)
        self.tearDownTempDirectory()
    
    
    def testShouldThrowExceptionIfRequirementsFileAbsent(self):
        pass
    
    # HELPER METHOD TESTS ----------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def testDictifyPipList(self):
        pass
    
    
    def testVersionUpdateScaleReturnsMajor(self):
        self.assertEqual(thaw.version_update_scale('1.0','2.1'),"major")
    
    def testVersionUpdateScaleReturnsMinor(self):
        self.assertEqual(thaw.version_update_scale('1.0.0','1.1.6'),"minor")
    
    def testVersionUpdateScaleReturnsMicro(self):
        self.assertEqual(thaw.version_update_scale('1.0.0','1.0.1'),"micro")
    
    def testVersionUpdateScaleReturnsNone(self):
        self.assertEqual(thaw.version_update_scale('1.0','1.0'),None)
    
    
    
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
        pass
    
    def testGetLatestVersion(self):
        pass
    
    
    # PROJECT SEARCH METHOD TESTS --------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    
    
    def testCheckFileForLibraryNoLibraryPresent(self):
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

if __name__ == '__main__':
    unittest.main()