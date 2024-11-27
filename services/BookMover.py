from core.Finder import FileFinder, Finder
from core.FileHandler import FileMover, FileService
import os
import pendulum
import subprocess
from itertools import chain
from collections import deque


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
        pathToBeVerified = self.bookPath
        if os.path.isdir(pathToBeVerified):
            return pathToBeVerified
        else:
            self.createDirectory(pathToBeVerified)
            return pathToBeVerified

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
        self.bookExtensions = deque(
            [
                'azw3$',
                'epub$',
                'mobi$',
                'pdf$',
                'djvu$',
                'chm$'
            ]
        )

    def move(self, destinationFilePath):
        bookFiles = self.gatherBookFilePaths(self.bookExtensions)
        if bookFiles:
            self.moveFiles(bookFiles, destinationFilePath)
        else:
            print("")
            print('[ INFO ] No More Book Files Left to Check')

    def gatherBookFilePaths(self, bookExtensions: deque):
        bookExtensions = self.bookExtensions
        accumulatedBookFiles: list[str] = list()

        for extension in bookExtensions:
            bookFilesForExtension = FileFinder(
                extension,
                self.path
            )
            bookFiles = Finder(bookFilesForExtension).find()
            if bookFiles:
                accumulatedBookFiles = list(chain(
                    accumulatedBookFiles,
                    bookFiles
                ))
            else:
                pass

        return accumulatedBookFiles

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


def moveBookFilesToBookFolder():
    bookPathParent = "/home/kayinfire/Documents/books/transferToOnedrive/"
    finalPath = DirectoryValidator(bookPathParent).execute()
    sourcePath = os.getenv('OLDPWD')
    BookFileMover(sourcePath).move(finalPath)

moveBookFilesToBookFolder()
