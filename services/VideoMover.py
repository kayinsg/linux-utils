import os
import subprocess
from core.Finder import FileFinder, Finder
from core.FileHandler import FileMover, FileService
# Note that this is a more extensible module than the FileSelector
# implemented within the original core classes


class FlexibleFileSelector:
    def __init__(self, registryPath):
        self.registryPath = registryPath

    def gatherDestinationPathFromUser(self):
        return self.readDestinationPathsFromRegistry()

    def readDestinationPathsFromRegistry(self):
        unixReadCommand = subprocess.run(
            ['cat', self.registryPath],
            check=True,
            capture_output=True,
            text=True
        )
        return self.allowUserToSelectDestinationPath(unixReadCommand.stdout)

    def allowUserToSelectDestinationPath(self, destinationRegistry):
        messageToUser = (
            "Select the Directory You'd Like To Move The Files To"
        )

        fileSelectorCommand = subprocess.run(
            ['fzf', f'--prompt={messageToUser}'],
            input=destinationRegistry,
            text=True,
            check=True,
            capture_output=True
        )

        userDestinationPath = self._truncateNewLineFromPath(fileSelectorCommand.stdout)
        return userDestinationPath

    def _truncateNewLineFromPath(self, path):
        cleanPath = path.strip()
        if cleanPath != path:
            print('The path had unparsable characters.')
            print('Cleaned Path:')
            print(cleanPath)
        return cleanPath


class VideoFileMover:
    def __init__(self, recipientDirectory):
        self.recipientDirectory = recipientDirectory

    def moveVideoFilesToPath(self, files, destinationDirectory):
        fileMover = FileMover(
            self.recipientDirectory,
            files,
            destinationDirectory
        )

        FileService(fileMover).executeCommand()


def findVideoFilesInDirectory(path):
    findCommand: object = FileFinder(
        "mp4",
        path
    )

    videoFilesWithinPath: list[str] = Finder(
        findCommand
    ).find()
    return videoFilesWithinPath


def main():
    videoLocations = "/home/kayinfire/Desktop/videoLocations"
    path = os.getenv('OLDPWD')

    videoFiles = findVideoFilesInDirectory(path)

    destinationPathSelector = FlexibleFileSelector(videoLocations)
    destinationPath = destinationPathSelector.gatherDestinationPathFromUser()

    VideoFileMover(path).moveVideoFilesToPath(videoFiles, destinationPath)


main()
