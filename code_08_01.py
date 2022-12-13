import numpy as np

inputFile = open("advent-of-code-2022-inputs/input_08.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

dat = [[int(y) for y in list(x.strip())] for x in inputDat]
datArr = np.array(dat)
visibleH = np.zeros_like(datArr)
visibleV = np.zeros_like(datArr.T)

for rr, row in enumerate(datArr):
    (leftCutoff, rightCutoff, leftPointer, rightPointer) = (-1, -1, 0, len(row) - 1)
    while((leftPointer < len(row)) & (leftCutoff < 9)):
        if(row[leftPointer] > leftCutoff):
            visibleH[rr, leftPointer] = 1
            leftCutoff = row[leftPointer]
        leftPointer +=1
    while((rightPointer >= 0) & (rightCutoff < 9)):
        if(row[rightPointer] > rightCutoff):
            visibleH[rr, rightPointer] = 1
            rightCutoff = row[rightPointer]
        rightPointer -=1

for rr, row in enumerate(datArr.T):
    (leftCutoff, rightCutoff, leftPointer, rightPointer) = (-1, -1, 0, len(row) - 1)
    while((leftPointer < len(row)) & (leftCutoff < 9)):
        if(row[leftPointer] > leftCutoff):
            visibleV[rr, leftPointer] = 1
            leftCutoff = row[leftPointer]
        leftPointer +=1
    while((rightPointer >= 0) & (rightCutoff < 9)):
        if(row[rightPointer] > rightCutoff):
            visibleV[rr, rightPointer] = 1
            rightCutoff = row[rightPointer]
        rightPointer -=1

visibleV = visibleV.T

visible = visibleH | visibleV
print(sum(sum(visible)))