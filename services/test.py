import unittest
from CodeLineCounter import FileGrouper, LineCounter
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

    def testShouldGetSLOCForeachFile(self):

        class FakeLineCounter(LineCounter):
            def __init__(self, listOfFiles):
                self.listOfFiles = listOfFiles

            def getNumber(self):
                return super().getNumber()

            def getlineCount(self, file):
                if file:
                    return 10
                return 10


        listOfFiles = ['example1.txt', 'mergesort.cpp', 'krralgorithm.py', 'django.py', 'react.js', 'init.lua']
        output = [
            {"example1.txt": 10},
            {"mergesort.cpp": 10},
            {"krralgorithm.py": 10},
            {"django.py": 10},
            {"react.js": 10},
            {"init.lua": 10}
        ]

        listOfLinesPerFile = FakeLineCounter(listOfFiles).getNumber()

        self.assertEqual(listOfLinesPerFile, output)



unittest.main(testRunner=ColourTextTestRunner())
