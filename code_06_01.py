inputFile = open("input/input_06.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

chars = list(inputDat[0])
last4 = chars[0:4]

index = 4
for c in chars[4:]:
    if(len(set(last4)) == len(last4)):
         break
    else:
        last4.pop(0)
        last4.append(c)
        index = index + 1

print(index)
