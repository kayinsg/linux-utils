import subprocess
from abc import ABC, abstractmethod
from re import finditer as findAllIterations
from collections import Counter


class FinderInterface(ABC):

    @abstractmethod
    def find(self) -> list[str]:
        raise NotImplementedError(
            'This is an abstract class.'
            'Subclasses must implement the find() method.'
        )


class FileFinder(FinderInterface):
    def __init__(self, pattern, path):
        self.pattern       = pattern
        self.path          = path

    def find(self):
        try:
            filesInPath = self.locateAllFiles()
            filesMatchingPattern = self.locateFilesMatchingPattern(
                filesInPath
            )
            return filesMatchingPattern
        except subprocess.CalledProcessError:
            print(
                '[ ERROR ] '
                'RipGrep was unable to find files matching '
                f'\"{self.pattern}\"'
            )

    def locateAllFiles(self):
        locateAllFilesCommand = []
        if self.path == "/home/kayinfire":
            locateAllFilesCommand = [
                'rg',
                '--files',
                f'{self.path}'
            ]
        else:
            locateAllFilesCommand = [
                'rg',
                '--files',
                '--hidden',
                f'{self.path}'
            ]
        filesWithinDirectory = subprocess.run(
            locateAllFilesCommand,
            text=True,
            check=True,
            stdout=subprocess.PIPE
        )
        return filesWithinDirectory.stdout

    def locateFilesMatchingPattern(self, filesInDirectory):
        findPattern = ['rg', f'{self.pattern}']

        filesMatchingPattern = subprocess.run(
            findPattern,
            input=filesInDirectory,
            text=True,
            check=True,
            capture_output=True,
        )
        finalOutput = filesMatchingPattern.stdout.splitlines()
        return finalOutput


class DirectoryFinder(FinderInterface):
    def __init__(self, listOfFiles):
        self.listOfFiles = listOfFiles

    def find(self) -> list[str]:
        filePaths                   = self.listOfFiles
        unorderedDirectoryPaths     = self.getDirectoryPaths(filePaths)
        directoryPathsSortedByDepth = self.getDirectoryPathsSortedByDepth(unorderedDirectoryPaths)
        return directoryPathsSortedByDepth

    def getDirectoryPaths(self, listOfPaths):
        directoryPaths = set(map(self._removeFileSuffix, listOfPaths))
        return list(directoryPaths)

    def _removeFileSuffix(self, filePath):
        searchEntriesIterator = findAllIterations("/", filePath)
        searchEntries         = list(searchEntriesIterator)
        positionOfFilePath    = searchEntries[-1].start()
        parentPath            = filePath[0:positionOfFilePath]
        return parentPath

    def getDirectoryPathsSortedByDepth(self, listOfFiles) -> list[str]:
        return sorted(listOfFiles, key = self.getNumberOfPathSeparators)

    def getNumberOfPathSeparators(self, paths):
        pathCounter = Counter(paths)
        numberOfPathSepartors = pathCounter['/']
        return numberOfPathSepartors


class Finder:
    def __init__(self, finder):
        self.finder = finder

    def find(self) -> list[str]:
        searchEntries = self.finder.find()
        return searchEntries
