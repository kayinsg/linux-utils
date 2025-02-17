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
from core.utils import copyPathToClipboard


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


class FileUtilsInterface(ABC):

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError("This is an abstract class")


class FileSelector(FileUtilsInterface):
    def __init__(self, searchEntries: list[str]) -> None:
        self.searchEntries = searchEntries
        fullTemporaryFilePath = Path(
            currentDirectory()
        ).joinpath('selectorEntries.txt')
        self.temporaryFile = fullTemporaryFilePath

    def execute(self) -> None:
        try:
            if self.searchEntries:
                self.writeLinesToTemporaryFile()
                filePath = self.letUserSelectFilePath()
                if filePath:
                    copyPathToClipboard(filePath)
                else:
                    print(
                        '[ INFO ] None Of The File Paths Have Been Copied To The Clipboard'
                    )
                remove(self.temporaryFile)
            else:
                print(
                    "[ ERROR ] "
                    "There Were No Results To Select "
                    "Through FZF From Your RipGrep Search."
                )
        except (TypeError, UnboundLocalError):
            print('[ ERROR ] Failed To Select File Path')

    def writeLinesToTemporaryFile(self):
        with open(self.temporaryFile, 'w') as file:
            for searchEntry in self.searchEntries:
                file.writelines(f"{searchEntry}\n")

    def letUserSelectFilePath(self):
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
    def __init__(self,
                 recipientDirectory,
                 files                  : list,
                 destinationDirectory   : str):

        self.recipientDirectory   = recipientDirectory
        self.files                = files
        self.destinationDirectory = path.expanduser(destinationDirectory)

    def execute(self) -> None:
        files       = self.files
        directory   = self.destinationDirectory
        if files:
            cleanedDirectory = self.ensureDirectoryExists(directory)
            returnValue = self.moveFiles(files, cleanedDirectory)
            self.displayCompletionToUser(returnValue)
        else:
            print('[ ERROR ] There Are No Files To Move')

    def ensureDirectoryExists(self, directory: str):
        try:
            checkDirectoryCommand = [
                'test', '-d', f'{directory}'
            ]
            directoryExists = subprocess.run(
                checkDirectoryCommand,
                capture_output=True,
                text=True,
                check=True
            ).returncode == 0

            if directoryExists:
                print("")
                print(f'[ SYSTEM INFO ] "{directory}" Exists')
                print('[ INFO ] Proceeding To Move Files.')
            else:
                self._createDirectory(directory)
                print(f"[ SYSTEM INFO ] CREATED FOLDER {directory}")
            return directory

        # except subprocess.CalledProcessError as error:
        except subprocess.CalledProcessError:
            # print(f'[ SYSTEM ERROR ] {error}')
            self._createDirectory(directory)
            print(f"[ SYSTEM INFO ] CREATED FOLDER {directory}")

    def _createDirectory(self, directory: str):
        try:
            subprocess.run(['mkdir', directory],
                           text  = True,
                           check = True)

        except subprocess.CalledProcessError as error:
            print('    An Issue Occured')
            print('    Directory Probably Already Exists')
            print('    Here Is The More Detailed Error Code:')
            print(f'        {error}')
            system.exit(1)

    def moveFiles(self, files: list[str], directory: str):
        for file in files:
            try:
                move(file, directory)
                print(
                    "[→] {} \nTRANSFERRED SUCCESSFULLY"
                    .format(file)
                )
                print("")
                fileIsTheLastOneBeingMoved = file == files[-1]
                if fileIsTheLastOneBeingMoved:
                    return True
            except (OSError, subprocess.CalledProcessError) as error:
                print("")
                print(f"[ SYSTEM ERROR ] {error}")
                return False

    def displayCompletionToUser(self, completionProcess: bool):
        print("")
        destinationDirectory = self.destinationDirectory
        if completionProcess:
            print(
                '[ INFO ] All Files Have Been '
                'Successfully Moved To "{}"'
                .format(destinationDirectory)
            )
            copyPathToClipboard(destinationDirectory)
        else:
            print(
                "[ ERROR ] "
                "Moving The Files Ultimately Turned Out To Be Unsuccessful"
            )


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
