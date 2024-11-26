import os
import subprocess
from core.Finder import FileFinder, Finder
from core.FileHandler import FileMover, FileService
# Note that this is a more extensible module than the FileSelector
# implemented within the original core classes


class FlexibleFileSelector:

    def readDestinationPathsFromRegistry(registryPath):
        unixReadCommand = subprocess.run(
            ['cat', registryPath],
            check=True,
            capture_output=True,
            text=True
        )
        return unixReadCommand.stdout

    def allowUserToSelectDestinationPath(filesFromRegistry):
        messageToUser = (
            "Select the Directory You'd Like To Move The Files To"
        )

        fileSelectorCommand = subprocess.run(
            ['fzf', f'--prompt={messageToUser}'],
            input=filesFromRegistry,
            text=True,
            check=True,
            capture_output=True
        )
        userDestinationPath = fileSelectorCommand.stdout
        return FlexibleFileSelector._truncateNewLineFromPath(userDestinationPath)

    def _truncateNewLineFromPath(path):
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

    destinationPaths = (
        FlexibleFileSelector.readDestinationPathsFromRegistry(videoLocations)
    )

    userDestinationPath = (
        FlexibleFileSelector.allowUserToSelectDestinationPath(destinationPaths)
    )

    VideoFileMover(path).moveVideoFilesToPath(videoFiles, userDestinationPath)


main()
