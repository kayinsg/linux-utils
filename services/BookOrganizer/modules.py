
from core.utils import fetchDirectoriesInPath, getListOfLinesFromFile
import subprocess
from core.FileHandler import FileMover
from core.utils import fetchDirectoriesInPath, getListOfLinesFromFile
import pathlib
from pathlib import Path
from core.FileHandler import FileMover
from services.BookOrganizer.pathNames import workingDirectory, StandardBooksPath, PDFPaths
import os

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
        FileMover(
            recipientDirectory   = self.workingDirectory,
            files                = standardBooks,
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
        FileMover(
            self.path['workingDirectory'],
            PDFDocuments,
            self.path['Documents']
        ).execute()

    def moveToBooksDirectory(self, PDFBooks: list[str]):
        FileMover(
            self.path['workingDirectory'],
            PDFBooks,
            self.path['Books']
        ).execute()

class MainPathRegistry:

    @staticmethod
    def createBookRegistryFile():
        home = Path.home().as_posix()
        return Path(os.path.join(home, "Desktop", "bookPathRegistry"))

    def __init__(self, bookPath):
        self.bookPath = bookPath
        self.fileContainingPersistentBookPaths = self.createBookRegistryFile()

    def retrieve(self) -> list[str]:
        bookRegistryAlreadyExits = self.fileContainingPersistentBookPaths.exists()
        if bookRegistryAlreadyExits:
            self.notifyUserOfExistingDirectory()
        else:
            return self.populateBookRegistry()
        return ['Main Folders Chosen By User']

    def notifyUserOfExistingDirectory(self):
        print(f'[ INFO ] "{self.fileContainingPersistentBookPaths}" already exists')
        print('Proceeding With Program')

    def populateBookRegistry(self):
        return RegistryPopulator(
            self.bookPath,
            self.fileContainingPersistentBookPaths
        ).get()


class RegistryPopulator:
    def __init__(self, bookPath, fileContainingPersistentBookPaths):
        self.bookPath = bookPath
        self.fileContainingPersistentBookPaths = fileContainingPersistentBookPaths

    def get(self):
        folders = self.getListOfFolders(self.bookPath)
        pathsChosenByUser = self.allowUserToSelectFolders(folders)
        self.storePathsInFile(pathsChosenByUser, self.fileContainingPersistentBookPaths)
        return pathsChosenByUser


    def getListOfFolders(self, path):
        itemsInPath = Path(path).iterdir()
        foldersInPath = list(filter(lambda item: item.is_dir(), itemsInPath))
        return list(
            map(
                lambda folder: str(folder),
                foldersInPath
            )
        )

    def allowUserToSelectFolders(self, foldersInBookPath):
        numberOfSelectedEntries = 0
        foldersChosenByUser = list()

        while numberOfSelectedEntries < 3:
            print(numberOfSelectedEntries)
            chosenEntry = self.allowUserToSelectFolderFromFZF(foldersInBookPath)
            foldersChosenByUser.append(chosenEntry)
            numberOfSelectedEntries+=1
        return foldersChosenByUser

    def allowUserToSelectFolderFromFZF(self, foldersInBookPath):
        return FZFMenu(foldersInBookPath).getPathFromUser()

    def storePathsInFile(self, paths, file):
        with open(file, 'w') as bookRegistry:
            for folder in paths:
                bookRegistry.writelines(f'{folder}\n')

class FZFMenu:
    def __init__(self, searchEntries):
        self.searchEntries = searchEntries
        self.temporaryFile = self.createTemporaryFilePath()

    @staticmethod
    def createTemporaryFilePath():
        currentDirectory = os.getcwd()
        return Path(
            os.path.join(currentDirectory, 'selectorEntries.txt')
        )

    def getPathFromUser(self):
        self.writeLinesToTemporaryFile()
        filePath = self.letUserSelectFilePath()
        os.remove(self.temporaryFile)
        return filePath.strip()

    def writeLinesToTemporaryFile(self):
        with open(self.temporaryFile, 'a') as file:
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
