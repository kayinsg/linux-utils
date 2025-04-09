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


class LineCounter:
    def __init__(self, listOfFiles):
        self.listOfFiles = listOfFiles

    @staticmethod
    def getlineCount(file):
        return subprocess.run(
            ['wc', '-l', f'{file}'],
            capture_output=True,
            text=True
        ).stdout.strip()

    def getNumber(self):
        fileSLOCHashTableWithoutTotals = list(map(self.aggregateFileWithSLOC, self.listOfFiles))
        return self.getFileSLOCHashTableWithTotals(fileSLOCHashTableWithoutTotals)

    def aggregateFileWithSLOC(self, file):
        numberOfLinesInFile = self.getlineCount(file)
        return {file: numberOfLinesInFile}

    def getFileSLOCHashTableWithTotals(self, fileSLOCHashTableWithoutTotals):
        return FileSLOCHashTable(fileSLOCHashTableWithoutTotals).finalizeTable()


class FileSLOCHashTable:
    def __init__(self, fileSLOCHashTableWithoutTotals):
        self.fileSLOCHashTableWithoutTotals = fileSLOCHashTableWithoutTotals

    def finalizeTable(self):
        total = self.summateTotalLineNumbersForAllFileSLOC(self.fileSLOCHashTableWithoutTotals)
        return self.getFinalHashTableForFileSLOC(self.fileSLOCHashTableWithoutTotals, total)

    def getFinalHashTableForFileSLOC(self, fileSLOCHashTableWithoutTotals, total):
        total = self.summateTotalLineNumbersForAllFileSLOC(fileSLOCHashTableWithoutTotals)
        fileSLOCHashTableWithoutTotals.append({'TOTAL': total})

        return fileSLOCHashTableWithoutTotals

    def summateTotalLineNumbersForAllFileSLOC(self, fileSLOCHashTableWithoutTotals):
        total = 0
        for item in fileSLOCHashTableWithoutTotals:
            for value in item.values():
                total += value
        return total
