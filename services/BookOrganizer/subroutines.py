# from pendulum import now as current
# import subprocess
from pathlib import Path, PurePath
# from os import getenv
from services.BookOrganizer.modules import (
        BookDirector,
        CurrentPath,
        MainPath,
        MainPathRegistry,
)
from services.BookOrganizer.dataTransferObjects import BookPathDetails


def backUpCurrentPath():
    booksBackupPath = createSubDirectoryDetails("transferToOnedrive")
    CurrentPath().backupBooks(booksBackupPath)


def moveBookFilesToSubs(subdir):
    bookPath = PurePath(Path.home(), 'Documents', 'books').as_posix()
    BookDirector(bookPath).move(subdir)


def getMainPathsFromUser():
    mainPath = createSubDirectoryDetails("")
    mainBookPathsFromUser = MainPathRegistry(mainPath).retrieve()
    return mainBookPathsFromUser


def moveSubDirBookFilesToMainSub(mainSubdirectory, exceptedFolders):
    MainPath(mainSubdirectory, exceptedFolders).moveBooks()


def createSubDirectoryDetails(subDir):
    home = Path.home()
    mainBookPath = PurePath(home / "Documents/books")
    fullPath = Path(mainBookPath).joinpath(subDir)
    return BookPathDetails(
        fullPath.as_posix(),
        mainBookPath.as_posix(),
        subDir
    )
