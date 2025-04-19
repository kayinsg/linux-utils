from core.FileHandler import FileDecompressor, FileService
import os

userPath = os.getenv('OLDPWD')

unzipper             = FileDecompressor(userPath)
FileService(unzipper).executeCommand()
