userPattern            = input("Please Enter The Pattern You are Searching For\n")
directorySearcher      = DirectoryFinder(fileSearchEntries)
directorySearchEntries = FileUtility.FinderContext(directorySearcher).find()
