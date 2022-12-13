inputFile = open("advent-of-code-2022-inputs/input_07.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

maxSize = 100000

class Directory:
    def __init__(self, path, parent):
        self.path = path
        self.parent = parent
        self.children = []
        self.size = 0
    
    def getSize(self):
        size = 0
        for child in self.children:
            size = size + child.getSize()
        self.size = size
        return size

    def addChild(self, child):
        self.children.append(child)

    def prettyPrint(self):
        if(self.parent is not None):
            print("Path: " + self.path + ", Parent: " + self.parent.path + ", Size: " + str(self.size))
        else:
            print("Path: " + self.path + ", Parent: None, Size: " + str(self.size))
        print("  Children:")
        for child in self.children:
            print("    " + child.path + ", Size: " + str(child.size))
        
class File:
    def __init__(self, path, parent, size):
        self.path = path
        self.parent = parent
        self.size = int(size)
    
    def getSize(self):
        return self.size

    def prettyPrint(self):
        print("Path: " + self.path + ", Parent: " + self.parent.path + ", Size: " + str(self.size))

currentDir = None
currentDirPath = ""
allDirs = {"/": Directory("/", None)}
allFiles = {}

for l in inputDat:
    if("$ ls" in l): # skip
        continue
    elif("$ cd /" in l): # return to root directory
        currentDir = allDirs["/"]
    elif("$ cd ..\n" in l): # return to parent directory
        currentDir = currentDir.parent
    elif("$ cd" in l): # change to new directory
        dirName = l.strip().split("cd")[-1].strip()
        currentDir = allDirs[currentDir.path + dirName + "/"]
    elif("dir " in l): # check if this is a new directory; if so, add to dict and make child of current directory
        dirName = l.strip().split(" ")[-1].strip()
        newDirPath = currentDir.path + dirName + "/"
        if(~(newDirPath in allDirs)):
            allDirs[newDirPath] = Directory(newDirPath, currentDir)
            currentDir.addChild(allDirs[newDirPath])
    else: # this is a file
        fileName = l.strip().split(" ")[-1].strip()
        fileSize = l.strip().split(" ")[0].strip()
        newFilePath = currentDir.path + fileName
        if(~(newFilePath in allFiles)):
            allFiles[newFilePath] = File(newFilePath, currentDir, fileSize)
            currentDir.addChild(allFiles[newFilePath])

sum = 0
for key in allDirs:
    allDirs[key].getSize()
    if(allDirs[key].size <= maxSize):
        sum = sum + allDirs[key].size

for key in allDirs:
    allDirs[key].prettyPrint()

print(sum)