import subprocess
from abc import ABC, abstractmethod
from pathlib import Path


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
        self.ripgrepCommand = self.determineSpecificLocateFilesCommand()

    def determineSpecificLocateFilesCommand(self):
        if self.path == Path.home():
            return [ 'rg', '--files', f'{self.path}' ]
        return [ 'rg', '--files', '--hidden', f'{self.path}']

    def find(self):
        filesInDirectory = self.locateAllFiles()
        filesMatchingPattern = self.locateFilesMatchingPattern(
            filesInDirectory,
            self.pattern
        )
        return filesMatchingPattern

    def locateAllFiles(self):
        filesWithinDirectory = subprocess.run(
            self.ripgrepCommand,
            text=True,
            check=True,
            stdout=subprocess.PIPE
        ).stdout
        return filesWithinDirectory

    def locateFilesMatchingPattern(self, filesInDirectory, pattern):
        try:
            filesMatchingPattern = subprocess.run(
                ['rg', f'{pattern}'],
                input=filesInDirectory,
                text=True,
                check=True,
                capture_output=True,
            ).stdout.splitlines()
            return filesMatchingPattern
        except subprocess.CalledProcessError:
            print(
                '[ ERROR ] '
                'RipGrep was unable to find files matching '
                f'\"{self.pattern}\"'
            )


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
