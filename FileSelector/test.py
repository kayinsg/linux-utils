from pathlib import Path
import unittest
from colour_runner.runner import ColourTextTestRunner
from NewFileSelector import (
    FileSearcher,
    UserMenu,
    Clipboard,
    TextEditor,
    FileClassifier,
    CommandLineParser,
    PDFReader,
    VLC,
    EbookReader
)


class CommandLineTests(unittest.TestCase):

    class FakeCommandLineArguments:
        def __init__(self, typeOfItemToSearch, patternToSearch):
            self.typeOfItemToSearch = typeOfItemToSearch
            self.patternToSearch = patternToSearch

    class FakeCommandLineParser(CommandLineParser):
        def __init__(self, cmdLineArguments):
            self.typeOfItem = cmdLineArguments.typeOfItemToSearch
            self.pattern = cmdLineArguments.patternToSearch

    def testShouldRunProgramGivenCorrectParameters(self):
        # GIVEN
        parameter1 = 'directories'
        parameter2 = 'patternExample'
        specificException = 'You have passed in parameters in the opposite way. Specify whether "files" or "directories first'
        cmdLineArguments = self.FakeCommandLineArguments(parameter1, parameter2)
        commandLineParser = self.FakeCommandLineParser(cmdLineArguments)
        # WHEN
        result = commandLineParser.validateParameters()
        # THEN
        self.assertEqual(result['pattern'], cmdLineArguments.patternToSearch )
        self.assertEqual(result['typeOfItem'], cmdLineArguments.typeOfItemToSearch )

    def testShouldRaiseExceptionGivenDirectoryParameterWasGivenLast(self):
        # GIVEN
        parameter1 = 'directories'
        parameter2 = 'patternExample'
        cmdLineArguments = self.FakeCommandLineArguments(parameter2, parameter1)
        specificException = 'You have passed in parameters in the opposite way. Specify "directories" first'
        # WHEN
        commandLineParser = self.FakeCommandLineParser(cmdLineArguments)
        # THEN
        with self.assertRaises(ValueError) as error:
            commandLineParser.validateParameters()

        self.assertEqual(str(error.exception), specificException)


    def testShouldRaiseExceptionWhenFilesParameterIsGivenLast(self):
        # GIVEN
        parameter1 = 'files'
        parameter2 = 'patternExample'
        specificException = 'You have passed in parameters in the opposite way. Specify "files" before pattern'
        cmdLineArguments = self.FakeCommandLineArguments(parameter2, parameter1)
        # WHEN
        commandLineParser = self.FakeCommandLineParser(cmdLineArguments)
        # THEN
        with self.assertRaises(ValueError) as error:
            commandLineParser.validateParameters()

        self.assertEqual(str(error.exception), specificException)


class FileSearcherTests(unittest.TestCase):

    class FakeFileSearcher(FileSearcher):
        def __init__(self, pattern):
            self.pattern = pattern

        def getItemsFromSearch(self):
            pass

    def testShouldRaiseErrorForFileSearchIfTypeOfItemIsIncorrect(self):
        pattern = ''
        incorrectParameter = 'character'
        fileSearcher = self.FakeFileSearcher(pattern)

        with self.assertRaises(ValueError) as error:
            fileSearcher.search(incorrectParameter)

        self.assertEqual(str(error.exception),'Type of item invalid. Permitted Options are "files" and "directories"')


class UserMenuTests(unittest.TestCase):

    def testShouldGetInputFromUser(self):

        class FakeFileSearcher(FileSearcher):
            def __init__(self, directory, pattern):
                self.directory = directory
                self.pattern = pattern

            def search(self):
                return ['a.txt\n',
                    'b.cpp \n',
                    'c.py\n',
                    'd.py\t\n',
                    'e.js\n',
                    'f.lua\n',
                    '\n',
            ]
        class FakeUserMenu(UserMenu):
            def __init__(self, filePathsForUser):
                self.filePathsForUser = filePathsForUser

            def displayMenuToUser(self, menuData):
                if menuData:
                    return self.filePathsForUser[2]
                else:
                    return "Fail"

        directory = ''
        searchPattern = 'py'
        listOfFiles = FakeFileSearcher(directory, searchPattern).search()
        menu = FakeUserMenu(listOfFiles)

        result = menu.allowUserToSelect()

        self.assertEqual(result, 'c.py\n')


class ClipboardTests(unittest.TestCase):

    class FakeClipboard(Clipboard):
        def __init__(self, path):
            self.path = path

        def copyPathToClipboard(self, path):
            self.copiedPath = path


    def testShouldCopyEnquotedUserSelectedFilePath(self):
        filePath = 'django.py'
        clipboard = self.FakeClipboard(filePath)

        clipboard.copy("quoted")

        self.assertEqual(clipboard.copiedPath, "'django.py'")

    def testShouldCopyUnquotedUserSelectedFilePath(self):
        filePath = 'django.py'
        clipboard = self.FakeClipboard(filePath)

        clipboard.copy("unquoted")

        self.assertEqual(clipboard.copiedPath, filePath)


class TextEditorTests(unittest.TestCase):

    class FakeTextEditor(TextEditor):
        def __init__(self, fileMetaData):
            self.fileMetaData = fileMetaData

        def openFileInTextEditor(self):
            self.fileRecevied = self.fileMetaData['file']

    def testShouldOpenPythonFileInNeofileRecevied(self):
        python = 'expense-tracker.py'
        fileMetaData = FileClassifier(python).getMetaData()
        textEditor = self.FakeTextEditor(fileMetaData)

        textEditor.open()

        self.assertEqual(textEditor.fileRecevied,  'expense-tracker.py')
    #
    def testShouldOpenHTMLFileInNeofileRecevied(self):
        html = 'index.html'
        fileMetaData = FileClassifier(html).getMetaData()
        textEditor = self.FakeTextEditor(fileMetaData)

        textEditor.open()

        self.assertEqual(textEditor.fileRecevied,  'index.html')

    # def testShouldOpenTxtFileInNeofileRecevied(self):
        # txt = 'instructions.txt'
        # fileMetaData = FileClassifier(txt).getMetaData()
        # textEditor = self.FakeTextEditor(fileMetaData)

        # textEditor.open()

        # self.assertEqual(textEditor.fileRecevied,  'instructions.txt')

    # def testShouldOpenHiddenFileInNeofileRecevied(self):
        # hiddenFile = '.gitconfig'
        # fileMetaData = FileClassifier(hiddenFile).getMetaData()
        # textEditor = self.FakeTextEditor(fileMetaData)

        # textEditor.open()

        # self.assertEqual(textEditor.fileRecevied,  '.gitconfig')

    # def testShouldOpenPlainFileInNeofileRecevied(self):
    #     plainFile = 'log'
    #     fileMetaData = FileClassifier(plainFile).getMetaData()
    #     textEditor = self.FakeTextEditor(fileMetaData)
    #
    #     textEditor.open()
    #
    #     self.assertEqual(textEditor.fileRecevied,  'log')

class VLCTests(unittest.TestCase):
    class FakeVLC(VLC):
        def __init__(self, fileMetaData):
            self.fileMetaData = fileMetaData

        def openFileInVLC(self):
            self.fileReceived = self.fileMetaData['file']

    def testShouldOpenFileInVLCGivenVideoFilePath(self):
        # GIVEN
        file = "ex.mp4"
        fileMetaData = FileClassifier(file).getMetaData()
        vlc = self.FakeVLC(fileMetaData)
        # WHEN
        vlc.open()
        # THEN
        self.assertEqual(vlc.fileReceived, "ex.mp4")
        
    def testShouldOpenFileInVLCGivenAudioFilePath(self):
        # GIVEN
        file = "ex.mp3"
        fileMetaData = FileClassifier(file).getMetaData()
        vlc = self.FakeVLC(fileMetaData)
        # WHEN
        vlc.open()
        # THEN
        self.assertEqual(vlc.fileReceived, "ex.mp3")
        

class PDFReaderTests(unittest.TestCase):

    class FakePDFReader(PDFReader):
        def __init__(self, fileMetaData):
            self.fileMetaData = fileMetaData

        def openFileInPDFReader(self):
            self.fileReceived = self.fileMetaData['file']


    def testShouldOpenPDFReaderWhenPdfFileIsGiven(self):
        # GIVEN
        pdfFile = "example.pdf"         
        fileMetaData = FileClassifier(pdfFile).getMetaData()
        pdfReader = self.FakePDFReader(fileMetaData)
        # WHEN
        pdfReader.open()
        # THEN
        # self.assertEqual(pdfReader.fileReceived, "example.pdf")
        

class EbookReaderTests(unittest.TestCase):

    class FakeEbookReader(EbookReader):
        def __init__(self, fileMetaData):
            self.fileMetaData = fileMetaData

        def openFileInEbookReader(self):
            self.file = self.fileMetaData['file']

    def testShouldOpenEbookReaderGivenEpub(self):
        # GIVEN the following preconditions corresponding to the system under test:
        epubFile = 'example.epub'
        fileMetaData = FileClassifier(epubFile).getMetaData()
        ebookReader = self.FakeEbookReader(fileMetaData)
        # WHEN the following module is executed:
        ebookReader.openFileInEbookReader()
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(ebookReader.file, 'example.epub')
        
        

if __name__ == '__main__':
    unittest.main(testRunner=ColourTextTestRunner())
