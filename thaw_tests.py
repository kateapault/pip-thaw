import unittest
from thaw import thaw

class ThawTests(unittest.TestCase):
    
    def testThawExists(self):
        pass
    
    
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