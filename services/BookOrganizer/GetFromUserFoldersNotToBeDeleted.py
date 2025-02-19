import subprocess
from pathlib import Path
import os

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
