import os

class FileGrouper:
    def __init__(self, directory):
        self.directory = directory

    def getSameTypeFiles(self, extension):
        filesInCurrentDirectory = self.getFilesInCurrentDirectory()
        path =  {self.directory: filesInCurrentDirectory}
        return self.getSimilarFilesInPath(path, extension)

    def getFilesInCurrentDirectory(self):
        return os.listdir(self.directory)

    def getSimilarFilesInPath(self, path, extension):
        result = []
        for files in path.values():
            for f in files:
                if f.endswith('.' + extension):
                    result.append(f)
        return result

