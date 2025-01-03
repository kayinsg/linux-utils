from pathlib import Path
import pyperclip


def fetchDirectoriesInPath(path: Path):
    elementsInDirectory = list(path.iterdir())

    foldersInPath = list()

    for pathInstance in elementsInDirectory:
        fullPath = pathInstance.as_posix()
        if pathInstance.is_dir():
            foldersInPath.append(fullPath)

    return foldersInPath


def getListOfLinesFromFile(filePath):
    if isinstance(filePath, Path):
        return filePath.read_text().splitlines()
    else:
        return Path(filePath).read_text().splitlines()


def copyPathToClipboard(filePath):
    sanitizedFilePath = filePath.strip()
    enclosedPath = f'"{sanitizedFilePath}"'
    pyperclip.copy(enclosedPath)
