import os
import subprocess

class FileGrouper:
    def __init__(self, extension):
        self.extension = extension

    def getSameTypeFiles(self):
        currentDirectory = self.getCurrentDirectory()
        filesInCurrentDirectory = self.getFilesInCurrentDirectory(currentDirectory)
        path =  {currentDirectory: filesInCurrentDirectory}
        return self.getSimilarFilesInPath(path, self.extension)

    def getCurrentDirectory(self):
        return subprocess.run('pwd', capture_output=True, text=True).stdout.strip()

    def getFilesInCurrentDirectory(self, directory):
        return os.listdir(directory)

    def getSimilarFilesInPath(self, path, extension):
        result = []
        for files in path.values():
            for f in files:
                if f.endswith('.' + extension):
                    result.append(f)
        return result
