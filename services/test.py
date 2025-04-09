import unittest
from CodeLineCounter import FileGrouper
from colour_runner.runner import ColourTextTestRunner

class SourceCodeRetrievalTest(unittest.TestCase):

    def testShouldGetListOfFilesThatAreTheSameType(self):

        class FakeFileGrouper(FileGrouper):
            def __init__(self, directory):
                self.directory = directory

            def getSameTypeFiles(self, extension):
                return super().getSameTypeFiles(extension)
            
            def getFilesInCurrentDirectory(self):
                return ['a.txt', 'b.cpp', 'c.py', 'd.py', 'e.js', 'f.lua']

        directory =  "/home/user1/Documents"
        relevantCodeFileNames = FakeFileGrouper(directory).getSameTypeFiles('py')

        self.assertEqual(relevantCodeFileNames, [ 'c.py', 'd.py' ])

unittest.main(testRunner=ColourTextTestRunner())
