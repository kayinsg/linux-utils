from core.FileHandler import FileMover, FileSelector, FileService
from os import remove, getenv
import pendulum
import subprocess
from pathlib import Path
from core.utils import fetchDirectoriesInPath, getListOfLinesFromFile


class BookPathGenerator:
    def __init__(self, parentPath):
        self.parentPath = parentPath

    def fetchFinalBookPath(self):
        date = self.getFormattedDate()
        prospectiveFileName = f"{date}-BooksToBeStored"
        return f"{self.parentPath}{prospectiveFileName}"

    def getFormattedDate(self):
        currentDate = pendulum.now()
        return currentDate.format("YYYY-MMM-DD")


class DirectoryValidator:
    def __init__(self, parentPath):
        self.bookPath = BookPathGenerator(parentPath).fetchFinalBookPath()

    def execute(self):
        pathToBeVerified = Path(self.bookPath)
        if pathToBeVerified.exists():
            return pathToBeVerified.as_posix()
        else:
            self.createDirectory(pathToBeVerified)
            return pathToBeVerified.as_posix()

    def createDirectory(self, directory):
        try:
            subprocess.run(['mkdir', directory],
                           text  = True,
                           check = True)
        except OSError:
            print("The Directory Already Exists.")


class BookFileMover:
    def __init__(self, path):
        self.path = path
        self.bookExtensions = [
                '*azw3',
                '*epub',
                '*mobi',
                '*pdf',
                '*djvu',
                '*chm'
        ]

    def move(self, destinationFilePath):
        bookFiles = self.getBookFiles(self.path, self.bookExtensions)
        if bookFiles:
            self.moveFiles(bookFiles, destinationFilePath)
        else:
            print("")
            print('[ INFO ] No More Book Files Left to Check')

    def getBookFiles(self, path, bookExtensions: list):
        sourcePath = Path(path)
        bookFilePaths: list = list()

        for extension in bookExtensions:
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

    def moveFiles(self, bookFiles, destinationFilePath):
        try:
            bookMover = FileMover(
                        recipientDirectory   = self.path,
                        files                = bookFiles,
                        destinationDirectory = destinationFilePath
                        )

            FileService(bookMover).executeCommand()
        except TypeError:
            print("")
            print('[ ERROR ] No Book Files To Move')


class PathRegistry:
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


def moveBookFilesToBookFolder():
    sourcePath = str(getenv('OLDPWD'))
    bookPathParent = "/home/kayinfire/Documents/books/transferToOnedrive/"
    finalPath = DirectoryValidator(bookPathParent).execute()
    BookFileMover(sourcePath).move(finalPath)


moveBookFilesToBookFolder()
