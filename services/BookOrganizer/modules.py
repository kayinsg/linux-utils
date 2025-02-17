from core.FileHandler import FileMover, FileSelector
from core.utils import fetchDirectoriesInPath, getListOfLinesFromFile
import pathlib
from pathlib import Path
from core.FileHandler import FileMover
from services.BookOrganizer.pathNames import workingDirectory, StandardBooksPath, PDFPaths

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


class Mover:
    def __init__(self, workingDirectory, standardBooksPath,PDFPaths):
        self.folder = pathlib.Path(workingDirectory)
        self.standardBooksPath = standardBooksPath
        self.PDFPaths = PDFPaths

    def move(self):
        files = self.getFilesInDirectory()
        StandardBookMover(self.folder.as_posix(), files).move(self.standardBooksPath)
        PDFMover(files, self.PDFPaths).move()

    def getFilesInDirectory(self):
        itemsInPath = list(
            map(
                lambda itemInFolder: itemInFolder,
                self.folder.iterdir()
            )
        )
        filesInPath = list(
            filter(
                lambda item: item.is_file(),
                itemsInPath
            )
        )
        return list(
            map(
                lambda itemName: itemName.as_posix(),
                filesInPath
            )
        )


class StandardBookMover:
    def __init__(self, workingDirectory:str, files: list[str]):
        self.workingDirectory = workingDirectory
        self.files = files
        self.bookExtensions = [
            'azw3',
            'epub',
            'mobi',
            'djvu',
            'chm',
        ]

    def move(self, standardBooksPath:str):
        standardBooks= list(
            filter(
                self.fileIsStandardBook,
                self.files
            )
        )
        self.moveBooks(standardBooks, standardBooksPath)

    def fileIsStandardBook(self, file: str):
        return list(
            filter(
                lambda extension: extension in file,
                self.bookExtensions
            )
        )

    def moveBooks(self, standardBooks: list[str], standardBooksDestinationPath):
        for book in standardBooks:
            pass
            FileMover(
                recipientDirectory   = self.workingDirectory,
                files                = list(book),
                destinationDirectory = standardBooksDestinationPath
            ).execute()


class PDFMover:
    def __init__(self, files: list[str], path:dict):
        self.files = files
        self.path = path

    def move(self):
        PDFItems = PDFHunter(self.files).getPDFs() 
        PDFTransporter(PDFItems, self.path).move()


class PDFHunter:
    def __init__(self, filesInPath):
        self.filesInPath = filesInPath
        self.years = list(
            map(
                lambda year: str(year),
                list(range(1960, 2026))
            )
        )

    def getPDFs(self):
        PDFFiles = list(filter(self.fileIsPDF, self.filesInPath))
        books = list(filter(self.PDFisBook, PDFFiles))
        documents = list(filter(self.PDFisDocument, PDFFiles))
        return {
            'Books': books,
            'Documents': documents,
        }

    def fileIsPDF(self, path):
        if path.lower().endswith('.pdf'):
            return True
        else:
            return False

    def PDFisBook(self, path):
        for year in self.years:
            if year in path:
                return True
        return False

    def PDFisDocument(self, path):
        for year in self.years:
            if year in path:
                return False
        return True


class PDFTransporter:
    def __init__(self, PDFfiles: dict, path: dict):
        self.PDFfiles = PDFfiles
        self.path = path

    def move(self):
        self.moveToDocumentsDirectory(self.PDFfiles['Documents'])
        self.moveToBooksDirectory(self.PDFfiles['Books'])

    def moveToDocumentsDirectory(self, PDFDocuments: list[str]):
        for document in PDFDocuments:
            FileMover(
                self.path['workingDirectory'],
                list(document),
                self.path['Documents']
            )

    def moveToBooksDirectory(self, PDFBooks: list[str]):
        for book in PDFBooks:
            pass
            FileMover(
                self.path['workingDirectory'],
                list(book),
                self.path['Books']
            )

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

Mover(workingDirectory, StandardBooksPath, PDFPaths).move()
