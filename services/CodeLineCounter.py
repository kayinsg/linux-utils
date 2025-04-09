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
        fileWithLineLength = list(map(self.aggregateFileWithSLOC, self.listOfFiles))
        return self.getFileSLOCHashTableWithTotals(fileWithLineLength)

    def aggregateFileWithSLOC(self, file):
        numberOfLinesInFile = self.getlineCount(file)
        return {file: numberOfLinesInFile}

    def getFileSLOCHashTableWithTotals(self, fileSLOCHashTable):
        return FileSLOCHashTable(fileSLOCHashTable).finalizeTable()


class FileSLOCHashTable:
    def __init__(self, fileWithLineLength):
        self.fileWithLineLength = fileWithLineLength

    def finalizeTable(self):
        total = self.summateTotalLineNumbersForAllFileSLOC(self.fileWithLineLength)
        return self.getFinalHashTableForFileSLOC(self.fileWithLineLength, total)

    def getFinalHashTableForFileSLOC(self, fileWithLineLength, total):
        total = self.summateTotalLineNumbersForAllFileSLOC(fileWithLineLength)
        fileWithLineLength.append({'TOTAL': total})

        return fileWithLineLength

    def summateTotalLineNumbersForAllFileSLOC(self, fileWithLineLength):
        total = 0
        for item in fileWithLineLength:
            for value in item.values():
                total += value
        return total
