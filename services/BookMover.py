from core.FileHandler import FileMover, FileSelector, FileService
from os import remove, getenv
from pendulum import now as current
import subprocess
from pathlib import Path, PurePath
from core.utils import fetchDirectoriesInPath, getListOfLinesFromFile


class BookDirector:
    def __init__(self, workingDirectory):
        self.workingDirectory = workingDirectory
        self.bookExtensions = [
                '*azw3',
                '*epub',
                '*mobi',
                '*pdf',
                '*djvu',
                '*chm'
        ]

    def move(self, destinationFilePath):
        bookFiles = self.getBookFilesInDirectory()
        if bookFiles:
            self.moveBookFilesToPath(bookFiles, destinationFilePath)
        else:
            print("")
            print('[ INFO ] No More Book Files Left to Check')

    def getBookFilesInDirectory(self):
        sourcePath = Path(self.workingDirectory)
        bookFilePaths: list = list()

        for extension in self.bookExtensions:
            listOfMatchingPathObjects = list(
                sourcePath.glob(extension)
            )

            if listOfMatchingPathObjects:
                for matchingPath in listOfMatchingPathObjects:
                    actualFilePath = matchingPath.absolute().as_posix()
                    bookFilePaths.append(actualFilePath)
            else:
                print(
                    f'[ SYSTEM INFO ] files containing the extension '
                    f'"{extension}" were unable to be found'
                )

        return bookFilePaths

    def moveBookFilesToPath(self, bookFiles, destinationFilePath):
        try:
            bookMover = FileMover(
                        recipientDirectory   = self.workingDirectory,
                        files                = bookFiles,
                        destinationDirectory = destinationFilePath
                        )

            FileService(bookMover).executeCommand()
        except TypeError:
            print("")
            print('[ ERROR ] No Book Files To Move')


class MainPathRegistry:
    def __init__(self, bookPath):
        self.bookPath = Path(
            bookPath
        )
        self.bookTemp = Path(
            self.bookPath / "folderRegistry.txt"
        )

    def retrieve(self):
        bookRegistryAlreadyExits = self.bookTemp.exists()
        if bookRegistryAlreadyExits:
            print(f'[ INFO ] "{self.bookTemp}" already exists')
            print('Proceeding With Program')
        else:
            foldersInPath = fetchDirectoriesInPath(self.bookPath)
            userMainFolders = self.getMainFoldersFromUser(foldersInPath)
            self.storeMainFoldersInFile(userMainFolders, self.bookTemp)

        return self.getListOfPathsFromRegistry(self.bookTemp)

    def getMainFoldersFromUser(self, foldersInPath: list):
        mainFolders: list = list()
        fileSelector = FileSelector(foldersInPath)
        fileSelector.writeLinesToTemporaryFile()
        while len(mainFolders) < 3:
            mainChosenByUser = fileSelector.letUserSelectFilePath()
            mainChosenByUser = mainChosenByUser.strip()
            mainFolders.append(mainChosenByUser)
        remove(fileSelector.temporaryFile)
        return mainFolders

    def storeMainFoldersInFile(self, mainFolders, bookTemp):
        with open(bookTemp, 'w') as mainFolderRegistryFolder:
            for folder in mainFolders:
                mainFolderRegistryFolder.writelines(f'{folder}\n')

    def getListOfPathsFromRegistry(self, tempFile):
        return getListOfLinesFromFile(tempFile)


def backupBookPath(path):
    date = current().format("YYYY-MMM-DD")
    backupFileDirectory = f"{date}-BooksToBeStored"
    finalBackupPath = Path(path / backupFileDirectory).as_posix()
    return finalBackupPath


def ensureDirectoryExists(path):
    pathToBeVerified = Path(path)
    if pathToBeVerified.exists():
        return pathToBeVerified.as_posix()
    else:
        try:
            subprocess.run(
                ['mkdir', pathToBeVerified.as_posix()],
                text=True,
                check=True
            )
            return pathToBeVerified.as_posix()
        except OSError:
            print("The Directory Already Exists.")


def transferCurrentPathBookFiles():
    sourcePath = str(getenv('OLDPWD'))
    backupPath = Path(Path.home() / 'Documents/books/transferToOnedrive')
    finalPath = DirectoryValidator(backupPath).execute()
    BookDirector(sourcePath).move(finalPath)


def moveBookFilesToSubs(targetPath):
    subPath = PurePath('Documents', 'books')
    sourcePath = Path(Path.home(), subPath).as_posix()
    BookDirector(sourcePath).move(targetPath)


transferCurrentPathBookFiles()
