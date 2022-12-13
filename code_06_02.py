inputFile = open("input/input_06.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

setNum = 14

chars = list(inputDat[0])
lastSet = chars[0:setNum]

index = setNum
for c in chars[setNum:]:
    if(len(set(lastSet)) == len(lastSet)):
         break
    else:
        lastSet.pop(0)
        lastSet.append(c)
        index = index + 1

print(index)
