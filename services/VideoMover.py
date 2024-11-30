import os
import subprocess
from core.Finder import FileFinder, Finder
from core.FileHandler import FileMover, FileService
from pathlib import Path


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
        workingDirectory = Path(path)
        videoFilesInDirectory = list()
        for videoFile in workingDirectory.glob('*.mp4'):
            videoFilesInDirectory.append(videoFile)

        return videoFilesInDirectory

    def moveVideoFilesToPath(self, files, destinationDirectory):
        fileMover = FileMover(
            self.recipientDirectory,
            files,
            destinationDirectory
        )

        FileService(fileMover).executeCommand()


class VideoOrganizer:
    def __init__(self, sourcePath, videoDestinationRegistry):
        self.sourcePath = sourcePath
        self.videoDestinationRegistry = videoDestinationRegistry

    def organize(self):
        workingPath = self.sourcePath
        destinationPath = self._getDestinationPathFromUser()
        VideoMover(workingPath).move(destinationPath)

    def _getDestinationPathFromUser(self):
        pathRegistry = self.videoDestinationRegistry
        destinationPath = (
            DestinationPathSelector(pathRegistry)
            .gatherDestinationPathFromUser()
        )
        return destinationPath


VideoOrganizer(
    os.getenv('OLDPWD'),
    "/home/kayinfire/Desktop/videoLocations"
).organize()
