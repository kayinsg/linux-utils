from core.Finder import FileFinder, Finder
from core.FileHandler import FileSelector, FileService
import os

previousDirectory = os.getenv('OLDPWD')
userPattern = input(
    "Please Enter The Pattern You are Searching For\n"
)


def getSearchEntries(userPattern, path) -> list[str]:
    fileSearcher           = FileFinder(userPattern, path)
    fileSearchEntries      = Finder(fileSearcher).find()
    return fileSearchEntries


def selectEntries(fileSearchEntries):
    selector               = FileSelector(fileSearchEntries)
    FileService(selector).executeCommand()


searchEntries = getSearchEntries(userPattern, previousDirectory)
selectEntries(searchEntries)
