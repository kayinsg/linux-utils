from shutil import move
import subprocess
from os import remove
from os import path
from os import getcwd as currentDirectory
from abc import ABC, abstractmethod
import re as regex
import sys as system
from pathlib import Path

from core.Finder import FileFinder, Finder
from core.utils import copyPathToClipboard, ZipFilePathDirectoryCreator

class FileUtilsInterface(ABC):

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError("This is an abstract class")


class FileSelector(FileUtilsInterface):
    def __init__(self, searchEntries: list[str]) -> None:
        self.searchEntries = searchEntries
        self.temporaryFile = self.createTemporaryFilePath()

    @staticmethod
    def createTemporaryFilePath():
        return Path(currentDirectory()).joinpath('selectorEntries.txt')

    def execute(self) -> None:
        searchEntriesFound = self.searchEntries is not None
        if searchEntriesFound:
            self.selectFromSearchEntries()
            remove(self.temporaryFile)
        else:
            self.notifyUserOfFailure()

    def selectFromSearchEntries(self):
        filePath = self.getUserChosenPath()
        if filePath:
            copyPathToClipboard(filePath)
        else:
            print(
                '[ INFO ] None Of The File Paths Have Been Copied To The Clipboard'
            )

    def getUserChosenPath(self):
        return FZFMenu(self.searchEntries, self.temporaryFile).getPathFromUser()

    def notifyUserOfFailure(self):
            print(
                "[ ERROR ] "
                "There Were No Results To Select "
                "Through FZF From Your RipGrep Search."
            )

class FZFMenu:
    def __init__(self, searchEntries, temporaryFile):
        self.searchEntries = searchEntries
        self.temporaryFile = temporaryFile

    def getPathFromUser(self):
        self.writeLinesToTemporaryFile()
        filePath = self.letUserSelectFilePath()
        return filePath

    def writeLinesToTemporaryFile(self):
        with open(self.temporaryFile, 'w') as file:
            for searchEntry in self.searchEntries:
                file.writelines(f"{searchEntry}\n")

    def letUserSelectFilePath(self):
        try:
            readFile = ['cat', self.temporaryFile]
            filePaths = subprocess.run(
                readFile, stdout=subprocess.PIPE, text=True
            ).stdout

            openPathInFZF = ['fzf']
            userSelectedFilePath = subprocess.run(
                openPathInFZF, input=filePaths, text=True,
                capture_output=True
            ).stdout

            return userSelectedFilePath
        except (TypeError, UnboundLocalError):
            print('[ ERROR ] Failed To Select File Path')


class FileDecompressor(FileUtilsInterface):
    def __init__(self, path):
        self.zipFiles: list = Finder(
            FileFinder("zip", path)
        ).find()

    def execute(self) -> None:
        zipFiles = self.zipFiles
        self.unzip(zipFiles)

    def unzip(self, zipFiles: list[str]):
        for file in zipFiles:
            folder = ZipFilePathDirectoryCreator(file).getFinalPath()
            try:
                subprocess.run(
                    ["unzip", "-d", folder, file],
                    text=True,
                    check=True,
                    capture_output=True
                )
            except subprocess.CalledProcessError as error:
                print(error)
                print(error.stderr)


class FileMover(FileUtilsInterface):
    def __init__(
        self,
        recipientDirectory   : str,
        files                : list,
        destinationDirectory : str,
    ):

        self.recipientDirectory   = recipientDirectory
        self.files                = files
        self.destinationDirectory = path.expanduser(destinationDirectory)

    def execute(self) -> None:
        if self.files:
            self.moveFiles(self.files, self.destinationDirectory)
        else:
            print('[ ERROR ] There Are No Files To Move')


    def moveFiles(
        self,
        files: list[str],
        destinationDirectory: str,
    ) -> None:
        try:
            DirectoryStockClerk(destinationDirectory).ensureDirectoryExists()
            self.moveFilesToDestinationPath(files, destinationDirectory)
            print(
                '\n'
                '[ INFO ] All Files Have Been '
                'Successfully Moved To "{}"'
                .format(destinationDirectory)
            )
        except OSError:
            print(
                "[ ERROR ] "
                "Moving The Files Ultimately Turned Out To Be Unsuccessful"
            )

    def moveFilesToDestinationPath(
        self,
        files: list[str],
        destinationPath: str,
    ) -> None:
        for file in files:
            try:
                move(file, destinationPath)
                print(
                    "[→] {} \nTRANSFERRED SUCCESSFULLY\n"
                    .format(file)
                )
            except (OSError, subprocess.CalledProcessError) as error:
                print("")
                print(f"[ SYSTEM ERROR ] {error}")


class DirectoryStockClerk:
    def __init__(self, directory: str):
        self.directory = directory

    def ensureDirectoryExists(self):
        if self._directoryExists():
            print("")
            print(f'[ SYSTEM INFO ] "{self.directory}" Exists')
        else:
            self._createDirectory()
            print(f"[ SYSTEM INFO ] CREATED FOLDER {self.directory}")

    def _directoryExists(self):
        checkDirectoryCommand = [
            'test', '-d', f'{self.directory}'
        ]
        directoryExists = subprocess.run(
            checkDirectoryCommand,
            capture_output=True,
            text=True,
            ).returncode == 0
        if directoryExists:
            return True
        return False

    def _createDirectory(self):
        try:
            subprocess.run(['mkdir', self.directory],
                           text  = True,
                           check = True)

        except subprocess.CalledProcessError as error:
            print('    An Issue Occured')
            print('    Directory Probably Already Exists')
            print('    Here Is The More Detailed Error Code:')
            print(f'        {error}')
            system.exit(1)


class FileDeleter(FileUtilsInterface):
    def __init__(self,
                 files: list,
                 directory):
        self.files     = files
        self.directory = directory

    def execute(self) -> None:
        self.deleteFiles()

    def deleteFiles(self) -> None:
        for file in self.files:
            remove(file)
        print("Files Have Been Removed")


class FileService:
    def __init__(self, fileOperation):
        self.fileOperation = fileOperation

    def executeCommand(self) -> None:
        self.fileOperation.execute()
