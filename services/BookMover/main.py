from modules import 
import subroutines

bookPath = "/home/kayinfire/Documents/books"
backupBookPathName = subroutines.backupBookPathName(bookPath)
finalBookPath = subroutines.ensureDirectoryExists(backupBookPathName)
