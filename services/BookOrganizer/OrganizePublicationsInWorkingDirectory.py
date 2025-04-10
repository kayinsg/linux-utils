from core.FileHandler import FileMover
import pathlib
from core.FileHandler import FileMover
from services.BookOrganizer.pathNames import workingDirectory, StandardBooksPath, PDFPaths

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
