from core.FileHandler import FileMover, FileSelector, FileService
from core.utils import fetchDirectoriesInPath, getListOfLinesFromFile
from pathlib import Path, PurePath
from os import remove, getenv
from pendulum import now as current
from os import getcwd

class CurrentPath:
    def backupBooks(self, pathDetails: BookPathDetails):
        backupBookPath = self.createBackupBookPathName(pathDetails.fullPath)
        workingDirectory = str(getenv('OLDPWD'))
        BookDirector(workingDirectory).move(backupBookPath)

    def createBackupBookPathName(self, path):
        date = current().format("YYYY-MMM-DD")
        backupFileDirectory = f"{date}-BooksToBeStored"
        finalBackupPath = PurePath(path, backupFileDirectory).as_posix()
        return finalBackupPath


class MainPath:
    def __init__(
        self,
        toBeOrganizedPath: BookPathDetails,
        exceptedFolders: list[str]
    ):
        self.toBeOrganizedPath = toBeOrganizedPath
        self.mainBookPath = toBeOrganizedPath.mainBookPath
        self.exceptedFolders = exceptedFolders

    def moveBooks(self):
        self.transferBooksInPathToMainSub()
        self.transferBooksFromSubsInPathToMainSub()

    def transferBooksFromSubsInPathToMainSub(self):
        mainBookPathContents = list(Path(self.mainBookPath).iterdir())
        for entry in mainBookPathContents:
            entryIsADirectory = entry.is_dir()
            if entryIsADirectory:
                path = entry.as_posix()
                if path in self.exceptedFolders:
                    pass
                else:
                    BookDirector(path).move(self.toBeOrganizedPath)
                    entry.rmdir()
            else:
                self.transferBooksInPathToMainSub()

    def transferBooksInPathToMainSub(self):
        BookDirector(self.mainBookPath).move(self.toBeOrganizedPath)


class BookDirector:
    def __init__(self, workingDirectory: str):
        self.workingDirectory = workingDirectory
        self.bookExtensions = [
            '*azw3',
            '*epub',
            '*mobi',
            '*djvu',
            '*chm',
            '*pdf',
        ]

    def move(self, destinationFilePath: BookPathDetails | str):
        bookFiles = self.getBookFilesInDirectory()
        if isinstance(destinationFilePath, str):
            if bookFiles:
                self.moveBookFilesToPath(
                    bookFiles,
                    destinationFilePath
                )
        if isinstance(destinationFilePath, BookPathDetails):
            if bookFiles:
                self.moveBookFilesToPath(
                    bookFiles,
                    destinationFilePath.fullPath
                )
        else:
            pass

    def getBookFilesInDirectory(self):
        sourcePath = Path(self.workingDirectory)
        bookFilePaths: list = list()

        for extension in self.bookExtensions:
            listOfMatchingPathObjects = list(sourcePath.glob(extension))

            if listOfMatchingPathObjects:
                for matchingPath in listOfMatchingPathObjects:
                    actualFilePath = matchingPath.absolute().as_posix()
                    bookFilePaths.append(actualFilePath)
            else:
                pass

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
    def __init__(self, bookPathDetails):
        self.bookPath = Path(
            bookPathDetails.mainBookPath
        )
        self.bookTemp = Path(
            self.bookPath / "folderRegistry.txt"
        )

    def retrieve(self) -> list[str]:
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
        with open(bookTemp, 'w') as mainFolderRegistryFile:
            for folder in mainFolders:
                mainFolderRegistryFile.writelines(f'{folder}\n')

    def getListOfPathsFromRegistry(self, tempFile):
        return getListOfLinesFromFile(tempFile)
