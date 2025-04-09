import os
import subprocess


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
    def __init__(self, listOfFiles):
        self.listOfFiles = listOfFiles

    def getTable(self):
        fileSLOCHashTableWithoutTotals = list(map(self.aggregateFileWithSLOC, self.listOfFiles))
        return self.getFileSLOCHashTableWithTotals(fileSLOCHashTableWithoutTotals)

    def aggregateFileWithSLOC(self, file):
        numberOfLinesInFile = self.getlineCount(file)
        return {file: numberOfLinesInFile}

    def getlineCount(self, file):
        return LineCounter(file).get()

    def getFileSLOCHashTableWithTotals(self, fileSLOCHashTableWithoutTotals):
        return FileSLOCHashTableWithTotals(fileSLOCHashTableWithoutTotals).finalizeTable()


class LineCounter:
    def __init__(self, file):
        self.file = file

    def get(self):
        numberOfLinesWithFileName = self.getNumberOfLinesDetails(self.file)
        return self.getOnlyTheFileNumber(numberOfLinesWithFileName)

    def getNumberOfLinesDetails(self, file):
        return subprocess.run(
            ['wc', '-l', f'{file}'],
            capture_output=True,
            text=True
        ).stdout.strip()

    def getOnlyTheFileNumber(self, numberOfLinesWithFileName):
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
