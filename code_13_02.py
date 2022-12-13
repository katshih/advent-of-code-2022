import ast

inputFile = open("input/input_13.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

def compareLists(left, right):
    index = 0

    while(index < max(len(left), len(right))):
        try:
            ll = left[index]
        except:
            return True
        try:
            rr = right[index]
        except:
            return False

        if((type(ll) is int) & (type(rr) is int)): # both are integers
            if(ll < rr):
                return True
            elif(rr < ll):
                return False
            else:
                index += 1
        else:
            if(type(ll) is int):
                ll = [ll]
            if(type(rr) is int):
                rr = [rr]
            subResult = compareLists(ll, rr)
            if(subResult == "Equal"):
                index += 1
            else:
                return subResult
    return "Equal"

class Packet():
    def __init__(self, list):
        self.list = list

    def __lt__(self, other):
        comp = compareLists(self.list, other.list)
        if(comp == "Equal"):
            comp = False
        return comp

dividers = [[[2]], [[6]]]

packetList = [Packet(x) for x in dividers]

for l in inputDat:
    if(len(l.strip()) == 0):
        continue
    packetList.append(Packet(ast.literal_eval(l)))

packetList.sort()
sortedLists = [p.list for p in packetList]

indexList = []
for d in dividers:
    indexList.append(sortedLists.index(d) + 1)

indexMult = 1
for i in indexList:
    indexMult *= i
print(indexMult)
