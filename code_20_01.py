inputFile = open("advent-of-code-2022-inputs/input_20.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

coordinates = [1000, 2000, 3000]

class cList():
    def __init__(self, itemsList):
        self.items = []

        itemObj = cItem(itemsList[0][0], itemsList[0][1])
        self.items.append(itemObj)
        for ii, item in enumerate(itemsList[1:]):
            itemObj = cItem(item[0], item[1], parent = self.items[ii])
            self.items.append(itemObj)
        for ii, item in enumerate(self.items):
            item.child = self.items[(ii + 1) % len(self.items)]
        self.items[0].parent = self.items[-1]

    def printValues(self, startIdx = 0):
        current = self.items[startIdx]
        for ii in range(0, len(self.items) - 1):
            print(str(current.value) + ',', end='')
            current = current.child
        print(str(current.value))

class cItem():
    def __init__(self, priority, value, parent = None, child = None):
        self.priority = priority
        self.value = value
        self.parent = parent
        self.child = child

    def getAncestor(self, num):
        currentAncestor = self
        for a in range(0, num):
            currentAncestor = currentAncestor.parent
            if(currentAncestor == self):
                currentAncestor = self.parent
        return currentAncestor

    def getDescendant(self, num):
        currentDescendant = self
        for c in range(0, num):
            currentDescendant = currentDescendant.child
            if(currentDescendant == self):
                currentDescendant = self.child
        return currentDescendant

    def __lt__(self, other):
        return self.priority < other.priority

    def __str__(self):
        return ("Priority: " + str(self.priority) + ", Value: " + str(self.value)
                    + ((", Parent P/V: " + str(self.parent.priority) + "/" + str(self.parent.value)) if self.parent is not None else ", no parent")
                    + ((", Child P/V: " + str(self.child.priority) + "/" + str(self.child.value)) if self.child is not None else ", no child"))

encrypted = []
for ii, l in enumerate(inputDat):
    encrypted.append((ii, int(l.strip())))

circle = cList(encrypted)

circle.items.sort()
# circle.printValues()
for item in circle.items:
    if(item.value > 0):
        insertAfter = item.getDescendant(item.value)
    elif(item.value < 0):
        insertAfter = item.getAncestor(abs(item.value) + 1)
    else:
        continue

    # reassign self.parent.child to self.child and self.child.parent to self.parent (e.g., remove from circle)
    item.parent.child = item.child
    item.child.parent = item.parent

    # reassign insertAfter.parent.child to self and insertAfter.child.parent to self (e.g., insert between)
    newChild = insertAfter.child
    insertAfter.child = item
    item.parent = insertAfter

    newChild.parent = item
    item.child = newChild
    # circle.printValues()

zeroPlace = [x for x in circle.items if(x.value == 0)][0]

sum = 0
for c in coordinates:
    currentDescendant = zeroPlace
    for a in range(0, c):
        currentDescendant = currentDescendant.child
    print(str(currentDescendant))
    sum += currentDescendant.value

print(sum)
