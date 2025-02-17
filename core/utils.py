from pathlib import Path
import pyperclip
import re as regex


def fetchDirectoriesInPath(path: Path):
    elementsInDirectory = list(path.iterdir())

    foldersInPath = list()

    for pathInstance in elementsInDirectory:
        fullPath = pathInstance.as_posix()
        if pathInstance.is_dir():
            foldersInPath.append(fullPath)

    return foldersInPath

def getListOfLinesFromFile(filePath):
    if isinstance(filePath, Path):
        return filePath.read_text().splitlines()
    else:
        return Path(filePath).read_text().splitlines()


def copyPathToClipboard(filePath):
    sanitizedFilePath = filePath.strip()
    enclosedPath = f'"{sanitizedFilePath}"'
    pyperclip.copy(enclosedPath)


class ZipFilePathDirectoryCreator:
    def __init__(self, zipFilePath):
        self.zipFilePath = zipFilePath

    def getFinalPath(self):
        basePath = self.getBaseDirectory(
            self.zipFilePath
        )
        actualFileName = self.getActualFileName(
            self.zipFilePath
        )
        fullPath = basePath + actualFileName

        self.createDirectory(fullPath)

        return fullPath

    def getBaseDirectory(self, filePath):
        directoryDelimiterPattern = regex.compile(r'/')
        delimiterMatches = regex.finditer(
            directoryDelimiterPattern, filePath
        )
        baseDirEnd = list(delimiterMatches)[3].start() + 1
        basePath = filePath[0:baseDirEnd]
        return basePath

    def getActualFileName(self, filePath):
        return self.getFileNameWithoutExtension(filePath)

    def getFileNameWithoutExtension(self, filePath: str) -> str:
        extensionMatch = regex.search(".zip", filePath).start()
        filename = filePath[:extensionMatch]
        return self.getFileNameFromPath(filename)

    def getFileNameFromPath(self, filePath: str) -> str:
        directoryDelimiterPattern = regex.compile(r'/')
        delimiterMatches = list(regex.finditer(
            directoryDelimiterPattern, filePath
        ))
        lastDelimiterIndex = list(delimiterMatches)[-1].start() + 1
        finalFilePathWithoutQuotes = filePath[lastDelimiterIndex:]
        return finalFilePathWithoutQuotes

    def createDirectory(self, directory: str):
        try:
            subprocess.run(['mkdir', directory],
                           text  = True,
                           check = True)
            print(f'[ SYSTEM INFO ] "{directory}" CREATED')

        except subprocess.CalledProcessError as error:
            print('[ INFO ] An Issue Occured '
                  'Perhaps The Directory Already Exists'
                  )
            print(f'[ SYSTEM INFO ] The Specific Error: {error}')
