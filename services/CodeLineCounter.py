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

    def getNumber(self):
        fileSLOCHashTableWithoutTotals = list(map(self.aggregateFileWithSLOC, self.listOfFiles))
        return self.getFileSLOCHashTableWithTotals(fileSLOCHashTableWithoutTotals)

    def aggregateFileWithSLOC(self, file):
        numberOfLinesInFile = self.getlineCount(file)
        return {file: numberOfLinesInFile}

    def getlineCount(self, file):
        return subprocess.run(
            ['wc', '-l', f'{file}'],
            capture_output=True,
            text=True
        ).stdout.strip()

    def getFileSLOCHashTableWithTotals(self, fileSLOCHashTableWithoutTotals):
        return FileSLOCHashTableWithTotals(fileSLOCHashTableWithoutTotals).finalizeTable()


class FileSLOCHashTableWithTotals:
    def __init__(self, fileSLOCHashTableWithoutTotals):
        self.fileSLOCHashTableWithoutTotals = fileSLOCHashTableWithoutTotals

    def finalizeTable(self):
        total = self.sumFileLineNumbers()
        return self.getFinalHashTableForFileSLOC(total)

    def sumFileLineNumbers(self):
        total = 0
        for item in self.fileSLOCHashTableWithoutTotals:
            for value in item.values():
                total += value
        return total

    def getFinalHashTableForFileSLOC(self, total):
        self.fileSLOCHashTableWithoutTotals.append({'TOTAL': total})
        return self.fileSLOCHashTableWithoutTotals
