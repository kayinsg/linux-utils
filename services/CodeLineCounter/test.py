import unittest
from CodeLineCounter import FileGrouper, FileSLOCHashTables, FileLineCounter
from colour_runner.runner import ColourTextTestRunner


class SourceCodeRetrievalTest(unittest.TestCase):

    def testShouldGetListOfFilesThatAreTheSameType(self):

        class FakeFileGrouper(FileGrouper):
            def __init__(self, directory):
                self.directory = directory

            def getFiles(self, extension):
                return super().getFiles(extension)
            
            def getFilesInCurrentDirectory(self):
                return ['a.txt', 'b.cpp', 'c.py', 'd.py', 'e.js', 'f.lua']

        directory =  "/home/user1/Documents"
        relevantCodeFileNames = FakeFileGrouper(directory).getFiles('py')

        self.assertEqual(relevantCodeFileNames, [ 'c.py', 'd.py' ])

    def testShouldGetTotalNumberOfLinesForSLOCHashTable(self):

        class FakeFileSLOCHashTables(FileSLOCHashTables):
            def __init__(self, listOfFiles, lineCounter):
                super().__init__(listOfFiles, lineCounter)

            def getTables(self):
                return super().getTables()

            def aggregateFileWithSLOC(self):
                return [
                    {"example1.txt": 10},
                    {"mergesort.cpp": 10},
                    {"krralgorithm.py": 10},
                    {"django.py": 10},
                    {"react.js": 10},
                    {"init.lua": 10}
                    ]

        listOfFiles = [ ]
        output =[
            {"example1.txt": 10},
            {"mergesort.cpp": 10},
            {"krralgorithm.py": 10},
            {"django.py": 10},
            {"react.js": 10},
            {"init.lua": 10},
            {'TOTAL': 60},
        ]
        lineCounter = ""

        result = FakeFileSLOCHashTables(listOfFiles, lineCounter).getTables()

        self.assertEqual(result, output)


    def testShouldConvertLinuxCommandOutputToHashmap(self):

        class FakeFileLineCounter(FileLineCounter):

            def getNumberOfLinesDetails(self, file):
                if file:
                    return '10 mergesort.cpp'

        fileName = 'mergesort.cpp'
        output = {'mergesort.cpp': 10}

        result = FakeFileLineCounter().get(fileName)

        self.assertEqual(result, output)

unittest.main(testRunner=ColourTextTestRunner())
