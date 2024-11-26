import subprocess
import pyperclip

def openFilePathsInFZF(self):
    readFile = ['cat', self.temporaryFile]
    filePaths = subprocess.run(readFile, stdout=subprocess.PIPE).stdout
    openPathInFZF = ['fzf'],
    userSelectedFilePath = subprocess.run(openPathInFZF, input = filePaths).stdout

def copyPathToClipboard(self, filePath):
    enclosedPath = f'"{filePath}"'
    pyperclip.copy(enclosedPath)
