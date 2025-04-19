import subprocess
import os
from pyperclip import copy
import sys


class CommandLineParser:
    def __init__(self, cmdLineArguments):
        self.typeOfItem = cmdLineArguments.typeOfItemToSearch
        self.pattern = cmdLineArguments.patternToSearch

    def validateParameters(self):
        self.checkIfFilesWasPassedInFirst()
        self.checkIfDirectoryWaspassedInFirst()
        return {'typeOfItem': self.typeOfItem, 'pattern': self.pattern}

    def checkIfFilesWasPassedInFirst(self):
        if self.typeOfItem != 'files' and self.pattern == 'files':
            raise ValueError('You have passed in parameters in the opposite way. Specify "files" before pattern')

    def checkIfDirectoryWaspassedInFirst(self):
        if self.typeOfItem != 'directories' and self.pattern == 'directories':
            raise ValueError('You have passed in parameters in the opposite way. Specify "directories" first')


class FileSearcher:
    def __init__(self, pattern):
        self.pattern = pattern

    def search(self, typeOfItem):
        if typeOfItem == "files":
            return self.getItemsFromSearch("file")
        if typeOfItem == "directories":
            return self.getItemsFromSearch("directory")
        else:
            raise ValueError('Type of item invalid. Permitted Options are "files" and "directories"')

    def getItemsFromSearch(self, flagType):
        return subprocess.run(
            ['fd', '-u', '-a', '--type', f'{flagType}', f'{self.pattern}'],
            check=True,
            capture_output=True,
            text=True
        ).stdout


class UserMenu:
    def __init__(self, filePathsForUser):
        self.filePathsForUser = filePathsForUser

    def allowUserToSelect(self):
        return self.displayMenuToUser(self.filePathsForUser)

    def displayMenuToUser(self, menuData):
        return subprocess.run(
            ['fzf'],
            capture_output=True,
            text=True,
            input=menuData
        ).stdout.strip()


class Clipboard:
    def __init__(self, path):
        self.path = path
    
    def copy(self, mode):
        enquotedFilePath = self.enquoteFilePath(mode)
        self.copyPathToClipboard(enquotedFilePath)

    def enquoteFilePath(self, mode):
        if mode == "quoted":
            return f"'{self.path}'"
        return self.path
    
    def copyPathToClipboard(self, path):
        copy(path)


class FileClassifier:
    def __init__(self, file):
        self.file = file

    def getMetaData(self):
        if self.fileIsACodeFile():
            return {'file': self.file, 'typeOfFile': 'editable'}
        elif self.fileIsMultiMedia():
            return {'file': self.file, 'typeOfFile':'multimedia'}
        elif self.fileIsAPdf():
            return {'file': self.file, 'typeOfFile':'PDF'}
        elif self.fileIsAnEbook():
            return {'file': self.file, 'typeOfFile':'ebook'}

    def fileIsACodeFile(self):
        if self.file.endswith('.py'):
            return True
        elif self.file.endswith('.html'):
            return True
        else:
            return False

    def fileIsMultiMedia(self):
        if self.file.endswith('.mp4'):
            return True
        elif self.file.endswith('.mp3'):
            return True
        elif self.file.endswith('.mkv'):
            return True
        elif self.file.endswith('.m4a'):
            return True
        elif self.file.endswith('.aac'):
            return True

    def fileIsAPdf(self):
        if self.file.endswith('.pdf'):
            return True

    def fileIsAnEbook(self):
        if self.file.endswith('.epub'):
            return True
        elif self.file.endswith('.mobi'):
            return True
        elif self.file.endswith('.azw3'):
            return True
        elif self.file.endswith('.azw'):
            return True
        elif self.file.endswith('.chm'):
            return True

    def fileIsAPlainTextFile(self):
        if self.file.endswith('.txt'):
            return True
        elif self.file.startswith('.'):
            return True
        else:
            pass


class TextEditor:
    def __init__(self, fileMetaData):
        self.fileMetaData = fileMetaData

    def open(self):
        if self.fileIsEditable():
            self.openFileInTextEditor()
        else:
            pass

    def fileIsEditable(self):
        if self.fileMetaData['typeOfFile'] == 'editable':
            return True
        else:
            pass

    def openFileInTextEditor(self):
        subprocess.run(['nvim', f'{self.fileMetaData["file"]}'])


class VLC:
    def __init__(self, fileMetaData):
        self.fileMetaData = fileMetaData

    def open(self):
        if self.fileIsPlayable():
            self.openFileInVLC()
        else:
            pass

    def fileIsPlayable(self):
        if self.fileMetaData['typeOfFile'] == 'multimedia':
            return True
        else:
            pass

    def openFileInVLC(self):
        subprocess.run(['vlc', f'{self.fileMetaData["file"]}'])


class PDFReader:
    def __init__(self, fileMetaData):
        self.fileMetaData = fileMetaData

    def open(self):
        if self.fileIsAPDF():
            self.openFileInPDFReader()
        else:
            pass

    def fileIsAPDF(self):
        if self.fileMetaData['typeOfFile'] == 'PDF':
            return True
        else:
            pass

    def openFileInPDFReader(self):
        pid = os.fork()
        if pid == 0:
            os.setsid()
            subprocess.Popen(
                ['zathura', self.fileMetaData["file"]],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True
            )
            os._exit(0)


class EbookReader:
    def __init__(self, fileMetaData):
        self.fileMetaData = fileMetaData

    def open(self):
        if self.fileIsAnEbook():
            self.openFileInEbookReader()
        else:
            pass

    def fileIsAnEbook(self):
        if self.fileMetaData['typeOfFile'] == 'ebook':
            return True
        else:
            pass

    def openFileInEbookReader(self):
        pid = os.fork()
        if pid == 0:
            os.setsid()
            subprocess.Popen(
                ['ebook-viewer', self.fileMetaData["file"]],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True
            )
            os._exit(0)
