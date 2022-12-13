import numpy as np

inputFile = open("input/input_08.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

dat = [[int(y) for y in list(x.strip())] for x in inputDat]
datArr = np.array(dat)
(left, right, top, bottom) = (np.zeros_like(datArr), np.zeros_like(datArr), np.zeros_like(datArr.T), np.zeros_like(datArr.T))

for rr, row in enumerate(datArr):
    visVals = np.ones((10,))
    (leftPointer, rightPointer) = (1, len(row) - 2)
    while((leftPointer < len(row))):
        left[rr, leftPointer] = visVals[row[leftPointer]]
        visVals[0:row[leftPointer] + 1] = 1
        visVals[row[leftPointer] + 1:] += 1
        leftPointer += 1

    visVals = np.ones((10,))    
    while((rightPointer >= 0)):
        right[rr, rightPointer] = visVals[row[rightPointer]]
        visVals[0:row[rightPointer] + 1] = 1
        visVals[row[rightPointer] + 1:] += 1
        rightPointer -= 1

for cc, col in enumerate(datArr.T):
    visVals = np.ones((10,))
    (topPointer, bottomPointer) = (1, len(col) - 2)
    while((topPointer < len(col))):
        top[cc, topPointer] = visVals[col[topPointer]]
        visVals[0:col[topPointer] + 1] = 1
        visVals[col[topPointer] + 1:] += 1
        topPointer += 1

    visVals = np.ones((10,))    
    while((bottomPointer >= 0)):
        bottom[cc, bottomPointer] = visVals[col[bottomPointer]]
        visVals[0:col[bottomPointer] + 1] = 1
        visVals[col[bottomPointer] + 1:] += 1
        bottomPointer -= 1
top = top.T
bottom = bottom.T

scores = np.multiply(np.multiply(left, right), np.multiply(top, bottom))
maxScore = np.max(scores)

print(maxScore)