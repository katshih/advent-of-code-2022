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

leftList = None
rightList = None
pairIndex = 0
sumIndices = 0

for l in inputDat:
    if(len(l.strip()) == 0):
        continue
    if(leftList is None):
        leftList = ast.literal_eval(l)
    elif(rightList is None):
        rightList = ast.literal_eval(l)

    if(rightList is not None):
        #print("Comparing " + str(leftList) + " and " + str(rightList))
        pairIndex += 1
        sumIndices += pairIndex*compareLists(leftList, rightList)
        (leftList, rightList) = (None, None)

print(sumIndices)