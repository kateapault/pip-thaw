import unittest
from thaw import thaw

class ThawTests(unittest.TestCase):
    
    def testThawExists(self):
        pass
    
    
    def testShouldThrowExceptionIfRequirementsFileAbsent(self):
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
    
    def testPackageInstanceNotSubwordReturnsFalseForSubwordAtEndOfWord(self):
        self.assertEqual(thaw.package_instance_not_subword('os','the kangaroos are wild'),False)
    
    def testPackageInstanceNotSubwordReturnsTrueForNoSubword(self):
        self.assertEqual(thaw.package_instance_not_subword('os','library os is in this line'),True)
    
    def testPackageInstanceNotSubwordRaisesExceptionIfPackageNameNotInString(self):
        pass
    
    
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

if __name__ == '__main__':
    unittest.main()