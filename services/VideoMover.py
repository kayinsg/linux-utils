import os
import subprocess
from core.Finder import FileFinder, Finder
from core.FileHandler import FileMover, FileService


class DestinationPathSelector:
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

        userDestinationPath = self._truncateNewLineFromPath(
            fileSelectorCommand.stdout
        )

        return userDestinationPath

    def _truncateNewLineFromPath(self, path):
        cleanPath = path.strip()
        return cleanPath


class VideoMover:
    def __init__(self, recipientDirectory):
        self.recipientDirectory = recipientDirectory

    def move(self, destinationPath):
        path = self.recipientDirectory
        videoFiles = self.findVideoFilesInDirectory(path)

        self.moveVideoFilesToPath(videoFiles, destinationPath)

    def findVideoFilesInDirectory(self, path: str):
        videoFilesWithinPath: list[str] = Finder(
            FileFinder("mp4", path)
        ).find()
        return videoFilesWithinPath

    def moveVideoFilesToPath(self, files, destinationDirectory):
        fileMover = FileMover(
            self.recipientDirectory,
            files,
            destinationDirectory
        )

        FileService(fileMover).executeCommand()


def main():
    videoLocations = (
        "/home/kayinfire/Desktop/videoLocations"
    )
    workingPath = os.getenv('OLDPWD')
    destinationPath = (
        DestinationPathSelector(videoLocations)
        .gatherDestinationPathFromUser()
    )
    VideoMover(workingPath).move(destinationPath)


main()
