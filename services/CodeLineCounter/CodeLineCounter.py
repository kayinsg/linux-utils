import os
import subprocess
import tabulate


class SLOCTabulator:
    def __init__(self, fileExtension):
        self.fileExtension = fileExtension
        self.directory = os.getcwd()

    def tabulateData(self):
        fileDetails = self.getHashTablesContainingFileNamesAndSLOC()
        tableData = self.convertListOfHashMapsToNestedList(fileDetails)
        return self.tabulateFileNameWithSourceLinesOfCode(tableData)

    def getHashTablesContainingFileNamesAndSLOC(self):
        listOfFiles = FileGrouper(self.directory).getFiles(self.fileExtension)
        lineCounter = FileLineCounter()
        return FileSLOCHashTables(listOfFiles, lineCounter).getTables()

    def convertListOfHashMapsToNestedList(self, hashTables):
        return HashmapToNestedList(hashTables).convert()

    def tabulateFileNameWithSourceLinesOfCode(self, tableData):
        return tabulate.tabulate(tableData, headers=["FILE", "NUMBER OF LINES"], tablefmt="grid")


class HashmapToNestedList:
    def __init__(self, hashTables):
        self.hashTables = hashTables
        self.tableData = [ ]

    def convert(self):
        fileNameSLOCList = list(map(self.createListOutofHashmap, self.hashTables))
        self.addListToTableData(fileNameSLOCList)
        return self.tableData

    def createListOutofHashmap(self, hashmap):
        key = list(hashmap.keys())[0]
        value = list(hashmap.values())[0]
        return [ key, value ]

    def addListToTableData(self, fileNameSLOCList):
        self.tableData.extend(fileNameSLOCList)


class FileGrouper:
    def __init__(self, directory):
        self.directory = directory

    def getFiles(self, extension):
        filesInCurrentDirectory = self.getFilesInCurrentDirectory()
        return self.getSimilarFilesInPath(filesInCurrentDirectory, extension)

    def getFilesInCurrentDirectory(self):
        return subprocess.run(
            ['rg', '--files'],
            check=True,
            capture_output=True,
            text=True
        ).stdout.splitlines()

    def getSimilarFilesInPath(self, files, extension):
        fileMatchesExtension = lambda file: self.fileMatchesExtension(file, extension)
        return list(filter(fileMatchesExtension, files))

    def fileMatchesExtension(self, file, extension):
        if file.endswith('.' + extension):
            return True
        return False


class FileSLOCHashTables:
    def __init__(self, listOfFiles, lineCounter):
        self.listOfFiles = listOfFiles
        self.lineCounter = lineCounter

    def getTables(self):
        fileSLOCHashTableWithoutTotals = self.aggregateFileWithSLOC()
        sortedHashTables = self.sortLineNumbersInSpecifiedOrder(fileSLOCHashTableWithoutTotals)
        return self.getFileSLOCHashTableWithTotals(sortedHashTables)

    def aggregateFileWithSLOC(self):
        getFileSLOCHashTableWithoutTotals = lambda file: self.lineCounter.get(file)
        return list(map(getFileSLOCHashTableWithoutTotals, self.listOfFiles))

    def sortLineNumbersInSpecifiedOrder(self, fileSLOCHashTableWithoutTotals):
        return LineNumberSorter(fileSLOCHashTableWithoutTotals).sortHashtables("descending")

    def getFileSLOCHashTableWithTotals(self, fileSLOCHashTableWithoutTotals):
        return FileSLOCHashTableWithTotals(fileSLOCHashTableWithoutTotals).finalizeTable()


class FileLineCounter:

    def get(self, file):
        numberOfLinesWithFileName = self.getNumberOfLinesDetails(file)
        fileName = self.getFileName(numberOfLinesWithFileName)
        lineNumber = self.getOnlyTheLineNumber(numberOfLinesWithFileName)
        return {fileName: lineNumber}

    def getNumberOfLinesDetails(self, file):
        return subprocess.run(
            ['wc', '-l', f'{file}'],
            capture_output=True,
            text=True
        ).stdout.strip()

    def getFileName(self, numberOfLinesWithFileName):
        return numberOfLinesWithFileName.split()[1]

    def getOnlyTheLineNumber(self, numberOfLinesWithFileName):
        return int(numberOfLinesWithFileName.split()[0])


class LineNumberSorter:
    def __init__(self, hashMapList):
        self.hashMapList = hashMapList

    def sortHashtables(self, sortingOrder):
        if sortingOrder == "descending":
            return sorted(self.hashMapList, key=self.sortInDescendingOrder)

    def sortInDescendingOrder(self, hashMap):
        return -list(hashMap.values())[0]


class FileSLOCHashTableWithTotals:
    def __init__(self, fileSLOCHashTables):
        self.fileSLOCHashTables = fileSLOCHashTables
        self.total = 0

    def finalizeTable(self):
        self.sumFileLineNumbers()
        self.addTotalLineNumbersToHashTable()
        return self.fileSLOCHashTables

    def sumFileLineNumbers(self):
        getTotalLines = lambda hashmap: self.getTotalNumberOfLinesInFile(hashmap)
        list(map(getTotalLines, self.fileSLOCHashTables))

    def getTotalNumberOfLinesInFile(self, hashmap):
        for value in hashmap.values():
            self.total += value

    def addTotalLineNumbersToHashTable(self):
        self.fileSLOCHashTables.append({'TOTAL': self.total})
