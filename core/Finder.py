import subprocess
from abc import ABC, abstractmethod
from re import finditer as findAllIterations


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
        ).stdout
        return filesWithinDirectory

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


# class DirectoryFinder(FinderInterface):
#     def __init__(self, listOfFiles):
#         self.listOfFiles = listOfFiles
#
#     def find(self) -> list[str]:
#

class Finder:
    def __init__(self, finder):
        self.finder = finder

    def find(self) -> list[str]:
        searchEntries = self.finder.find()
        return searchEntries

    # def findDirectories(self):
    #     filesInDirectory = self.find()
    #     return DirectoryFinder(filesInDirectory).find()
