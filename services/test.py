import unittest
from CodeLineCounter import FileGrouper, FileSLOCHashTable, LineCounter
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

    def testShouldGetTotalNumberOfLinesForSLOCHashTable(self):

        class FakeFileSLOCHashTable(FileSLOCHashTable):
            def __init__(self, listOfFiles, lineCounter):
                super().__init__(listOfFiles, lineCounter)

            def getTable(self):
                return super().getTable()

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

        result = FakeFileSLOCHashTable(listOfFiles, lineCounter).getTable()

        self.assertEqual(result, output)


    def testShouldConvertLinuxCommandOutputToHashmap(self):

        class FakeLineCounter(LineCounter):

            def getNumberOfLinesDetails(self, file):
                if file:
                    return '10 mergesort.cpp'

        fileName = 'mergesort.cpp'
        output = {'mergesort.cpp': 10}

        result = FakeLineCounter().get(fileName)

        self.assertEqual(result, output)

unittest.main(testRunner=ColourTextTestRunner())
