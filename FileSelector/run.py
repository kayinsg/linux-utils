from NewFileSelector import CommandLineParser, FileSearcher, UserMenu, Clipboard, FileClassifier, TextEditor
import argparse
import sys
from NewFileSelector import (
    CommandLineParser,
    FileSearcher,
    UserMenu,
    Clipboard,
    FileClassifier,
    TextEditor,
    PDFReader,
    VLC,
    EbookReader
)


parser = argparse.ArgumentParser(description="Searcher Program")
parser.add_argument('typeOfItemToSearch', type=str, help='Specify whether you are searching for files or directories')
parser.add_argument('patternToSearch', type=str, help='Specify the Path to Search in REGEX Syntax')
args = parser.parse_args()

def search():
    try:
        parameters = CommandLineParser(args).validateParameters()
        listOfFiles = FileSearcher(parameters['pattern']).search(parameters['typeOfItem'])
        fileChosenByUser = UserMenu(listOfFiles).allowUserToSelect()
        Clipboard(fileChosenByUser).copy("quoted")
        metadata = FileClassifier(fileChosenByUser).getMetaData()
        TextEditor(metadata).open()
        PDFReader(metadata).open()
        EbookReader(metadata).open()
        VLC(metadata).open()
    except ValueError as error:
        print(str(error))
    except (TypeError) as none:
        print('ERROR: You did not select a File Path. Exiting Program')
        sys.exit(1)

search()
