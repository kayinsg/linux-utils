import os
import subprocess
from core.FileHandler import FileMover, FileService
from pathlib import Path


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
        destinationPath = DestinationPathSelector(pathRegistry).getPath()
        return destinationPath


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
        try:
            fileMover = FileMover(
                self.recipientDirectory,
                files,
                destinationDirectory
            )

            FileService(fileMover).executeCommand()
        except TypeError as error:
            if "None" in str(error):
                print('[ INFO ] There were No Files To Be Moved')
            else:
                print('[ INFO ] Video Files Were Unable to Be Moved')
                print(error)


class DestinationPathSelector:
    def __init__(self, registryPath):
        self.registryPath = registryPath

    def getPath(self):
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
        try:
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
        except subprocess.SubprocessError:
            print('[ INFO ] You Have Exited The File Selection')

    def _truncateNewLineFromPath(self, path):
        cleanPath = path.strip()
        return cleanPath


VideoOrganizer(
    os.getenv('OLDPWD'),
    "/home/kayinfire/Desktop/videoLocations"
).organize()
