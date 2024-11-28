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


class VideoOrganizer:
    def __init__(self, videoDestinationRegistry, sourcePath, destinationPath):
        self.videoDestinationRegistry = videoDestinationRegistry
        self.sourcePath = sourcePath
        self.destinationPath = self._getDestinationPathFromUser()

    def organize(self):
        workingPath = self.sourcePath
        destinationPath = self.destinationPath
        VideoMover(workingPath).move(destinationPath)

    def _getDestinationPathFromUser(self):
        pathRegistry = self.videoDestinationRegistry
        destinationPath = (
            DestinationPathSelector(pathRegistry)
            .gatherDestinationPathFromUser()
        )
        return destinationPath
