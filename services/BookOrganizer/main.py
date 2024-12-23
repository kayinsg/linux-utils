from services.BookOrganizer.subroutines import (
    backUpCurrentPath,
    moveBookFilesToSubs,
    getMainPathsFromUser,
    moveSubDirBookFilesToMainSub,
    createSubDirectoryDetails,
)

backUpCurrentPath()
mainPaths = getMainPathsFromUser()
toBeOrganizedPath = createSubDirectoryDetails("main/toBeOrganized")
moveBookFilesToSubs(toBeOrganizedPath)
moveSubDirBookFilesToMainSub(toBeOrganizedPath, mainPaths)
