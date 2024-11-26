import FileUtility

userPattern          = input("Please Enter The Pattern You are Searching For\n")
destinationDirectory = input("What is The Destination Directory?\n")

def returnSearchEntriesThatMatchPattern(userPattern) -> list[str]:
    searchResults        = FileUtility.FileFinder(userPattern)
    fileMatches          = FileUtility.FinderContext(searchResults).find()
    return fileMatches


def moveFilesToDirectory(fileMatches, destinationDirectory) -> None:
    mover                = FileUtility.FileMover(fileMatches, destinationDirectory)
    FileUtility.FileContext(mover).executeCommand()

fileMatches = returnSearchEntriesThatMatchPattern(userPattern)
moveFilesToDirectory(fileMatches, destinationDirectory)
