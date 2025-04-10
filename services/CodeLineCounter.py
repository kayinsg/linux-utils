import os
import subprocess
import tabulate


class SLOCTabulator:
    def __init__(self, fileExtension):
        self.fileExtension = fileExtension

    def tabulateData(self):
        fileDetails = self.getHashTableContainingFileDetails()
        return self.tabulateFileNameWithLinesOfCode(fileDetails)

    def getHashTableContainingFileDetails(self):
        listOfFiles = FileGrouper(os.getcwd()).getSameTypeFiles(self.fileExtension)
        lineCounter = LineCounter()
        return FileSLOCHashTable(listOfFiles, lineCounter).getTable()

    def tabulateFileNameWithLinesOfCode(self, hashTable):
        tableData = []
        for item in hashTable:
            key = list(item.keys())[0]
            value = list(item.values())[0]
            tableData.append([key, value])
        return tabulate.tabulate(tableData, headers=["FILE", "NUMBER OF LINES"], tablefmt="grid")


class FileGrouper:
    def __init__(self, directory):
        self.directory = directory

    def getSameTypeFiles(self, extension):
        filesInCurrentDirectory = self.getFilesInCurrentDirectory()
        return self.getSimilarFilesInPath(filesInCurrentDirectory, extension)

    def getFilesInCurrentDirectory(self):
        return os.listdir(self.directory)

    def getSimilarFilesInPath(self, files, extension):
        fileMatchesExtension = lambda file: self.fileMatchesExtension(file, extension)
        return list(filter(fileMatchesExtension, files))

    def fileMatchesExtension(self, file, extension):
        if file.endswith('.' + extension):
            return True
        return False


class FileSLOCHashTable:
    def __init__(self, listOfFiles, lineCounter):
        self.listOfFiles = listOfFiles
        self.lineCounter = lineCounter

    def getTable(self):
        fileSLOCHashTableWithoutTotals = self.aggregateFileWithSLOC()
        return self.getFileSLOCHashTableWithTotals(fileSLOCHashTableWithoutTotals)

    def aggregateFileWithSLOC(self):
        getFileSLOCHashTableWithoutTotals = lambda file: self.lineCounter.get(file)
        return list(map(getFileSLOCHashTableWithoutTotals, self.listOfFiles))

    def getFileSLOCHashTableWithTotals(self, fileSLOCHashTableWithoutTotals):
        return FileSLOCHashTableWithTotals(fileSLOCHashTableWithoutTotals).finalizeTable()


class LineCounter:

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


class FileSLOCHashTableWithTotals:
    def __init__(self, fileSLOCHashTableWithoutTotals):
        self.fileSLOCHashTableWithoutTotals = fileSLOCHashTableWithoutTotals

    def finalizeTable(self):
        total = self.sumFileLineNumbers()
        self.addTotalLineNumbersToHashTable(total)
        return self.fileSLOCHashTableWithoutTotals

    def sumFileLineNumbers(self):
        total = 0
        for item in self.fileSLOCHashTableWithoutTotals:
            for value in item.values():
                total += value
        return total

    def addTotalLineNumbersToHashTable(self, total):
        self.fileSLOCHashTableWithoutTotals.append({'TOTAL': total})
