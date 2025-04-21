import unittest
from colour_runner.runner import ColourTextTestRunner
from CodeLineCounter import FileGrouper, FileSLOCHashTables, FileLineCounter, LineNumberSorter

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
                    {"example1.txt": 23},
                    {"mergesort.cpp": 57},
                    {"krralgorithm.py": 43},
                    {"django.py": 79},
                    {"react.js": 91},
                    {"init.lua": 89}
                    ]

        # TO DO: ADAPT THE NEW OUPUT with total to the sorted functionality
        listOfFiles = [ ]
        output =[
            {"example1.txt": 23},
            {"mergesort.cpp": 57},
            {"krralgorithm.py": 43},
            {"django.py": 79},
            {"react.js": 91},
            {"init.lua": 89},
            {'TOTAL': 382},
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

    def testShouldSortFileNamesByNumberOfLinesInDescendingOrder(self):
        inputData =[
            {"example1.txt": 23},
            {"mergesort.cpp": 57},
            {"krralgorithm.py": 43},
            {"django.py": 79},
            {"react.js": 91},
            {"init.lua": 89},
        ]

        outputData = [
            {"react.js": 91},
            {"init.lua": 89},
            {"django.py": 79},
            {"mergesort.cpp": 57},
            {"krralgorithm.py": 43},
            {"example1.txt": 23}
        ]

        result = LineNumberSorter(inputData).sortHashtables("descending")

        self.assertEqual(result, outputData)

if __name__ == '__main__':
    unittest.main(testRunner=ColourTextTestRunner())
