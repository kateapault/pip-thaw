import unittest
from thaw import thaw

class ThawTests(unittest.TestCase):
    
    def thawExists(self):
        pass
    
    def shouldThrowExceptionIfRequirementsFileAbsent(self):
        pass
    
    
    
    
    def versionUpdateScaleReturnMajor(self):
        pass
    
    def versionUpdateScaleReturnMinor(self):
        pass
    
    def versionUpdateScaleReturnMicro(self):
        pass
    
    def versionUpdateScaleReturnNone(self):
        pass
    
    
    
    def checkPackageNameIsntSubwordReturnsFalseForSubwordInMiddleOfWord(self):
        pass
    
    def checkPackageNameIsntSubwordReturnsFalseForSubwordAtBeginningOfWord(self):
        pass
    
    def checkPackageNameIsntSubwordReturnsFalseForSubwordAtEndOfWord(self):
        pass
    
    def checkPackageNameIsntSubwordReturnsTrueForNoSubword(self):
        pass
    
    def checkPackageNameIsntSubwordRaisesExceptionIfPackageNameNotThere(self):
        pass
    
    
    def checkFileForLibraryNoLibraryPresent(self):
        pass
    
    def checkFileForLibraryImportLibrary(self):
        pass
    
    def checkFileForLibraryFromLibraryImportOneModule(self):
        pass
    
    def checkFileForLibraryFromLibraryImportTwoModules(self):
        pass

    def checkFileForLibraryImportLibraryAsAlias(self):
        pass
    
    def checkFileForLibraryFromLibraryImportOneModuleAsAlias(self):
        pass
    
    def checkFileForLibraryAndIdentifyVariables(self):
        pass

if __name__ == '__main__':
    unittest.main()