from pendulum import now as current
import subprocess
from pathlib import Path, PurePath
from os import getenv
from modules import BookDirector, MainPathRegistry


def backupBookPathName(path):
    date = current().format("YYYY-MMM-DD")
    backupFileDirectory = f"{date}-BooksToBeStored"
    finalBackupPath = Path(path / backupFileDirectory).as_posix()
    return finalBackupPath


def ensureDirectoryExists(path):
    pathToBeVerified = Path(path)
    if pathToBeVerified.exists():
        return pathToBeVerified.as_posix()
    else:
        try:
            subprocess.run(
                ['mkdir', pathToBeVerified.as_posix()],
                text=True,
                check=True
            )
            return pathToBeVerified.as_posix()
        except OSError:
            print("The Directory Already Exists.")


def transferCurrentPathBookFiles(backupPath):
    sourcePath = str(getenv('OLDPWD'))
    backupPath = Path(Path.home() / 'Documents/books/transferToOnedrive')
    BookDirector(sourcePath).move(backupPath)


def moveBookFilesToSubs(targetPath):
    subPath = PurePath('Documents', 'books')
    sourcePath = Path(Path.home(), subPath).as_posix()
    BookDirector(sourcePath).move(targetPath)
