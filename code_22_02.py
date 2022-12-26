# 114399 is too high
# 5204 is too high

import numpy as np
import re

inputString = "advent-of-code-2022-inputs/input_22.txt"
inputFile = open(inputString, "r")
inputDat = inputFile.readlines()
inputFile.close()

instructions = [x for x in re.split('(\d+)', inputDat[-1][0:-1]) if x != '']

map = []
for l in inputDat[0:-2]:
    map.append([-1 if (x == ' ') else (0 if (x == '.') else 1) for x in list(l[0:-1])])
(numRows, numCols) = (len(map), 1)
for row in map:
    numCols = max(numCols, len(row))
for row in map:
    numAppend = numCols - len(row)
    if(numAppend > 0):
        row.extend([-1 for x in range(0, numAppend)])
map = np.array(map)

cubeSides = {}
if(inputString == "advent-of-code-2022-inputs/input_22_test.txt"):
    (maxRow, maxCol) = (4, 4)
    cubeSides['1'] = {'map': map[0:4, 8:12], 'offset': (0, 8), 'left': ('3', 'top'), 'top': ('2', 'top'), 'right': ('6', 'right'), 'bottom': ('4', 'top')}
    cubeSides['2'] = {'map': map[4:8, 0:4], 'offset': (4, 0), 'left': ('6', 'bottom'), 'top': ('1', 'top'), 'right': ('3', 'left'), 'bottom': ('5', 'bottom')}
    cubeSides['3'] = {'map': map[4:8, 4:8], 'offset': (4, 4), 'left': ('2', 'right'), 'top': ('1', 'left'), 'right': ('4', 'left'), 'bottom': ('5', 'left')}
    cubeSides['4'] = {'map': map[4:8, 8:12], 'offset': (4, 8), 'left': ('3', 'right'), 'top': ('1', 'bottom'), 'right': ('6', 'top'), 'bottom': ('5', 'top')}
    cubeSides['5'] = {'map': map[8:12, 8:12], 'offset': (8, 8), 'left': ('3', 'bottom'), 'top': ('4', 'top'), 'right': ('6', 'left'), 'bottom': ('2', 'bottom')}
    cubeSides['6'] = {'map': map[8:12, 12:16], 'offset': (8, 12), 'left': ('5', 'right'), 'top': ('4', 'right'), 'right': ('1', 'right'), 'bottom': ('2', 'left')}
elif(inputString == "advent-of-code-2022-inputs/input_22.txt"):
    (maxRow, maxCol) = (50, 50)
    cubeSides['1'] = {'map': map[0:50, 50:100], 'offset': (0, 50), 'left': ('4', 'left'), 'top': ('6', 'left'), 'right': ('2', 'left'), 'bottom': ('3', 'top')}
    cubeSides['2'] = {'map': map[0:50, 100:150], 'offset': (0, 100), 'left': ('1', 'right'), 'top': ('6', 'bottom'), 'right': ('5', 'right'), 'bottom': ('3', 'right')}
    cubeSides['3'] = {'map': map[50:100, 50:100], 'offset': (50, 50), 'left': ('4', 'top'), 'top': ('1', 'bottom'), 'right': ('2', 'bottom'), 'bottom': ('5', 'top')}
    cubeSides['4'] = {'map': map[100:150, 0:50], 'offset': (100, 0), 'left': ('1', 'left'), 'top': ('3', 'left'), 'right': ('5', 'left'), 'bottom': ('6', 'top')}
    cubeSides['5'] = {'map': map[100:150, 50:100], 'offset': (100, 50), 'left': ('4', 'right'), 'top': ('3', 'bottom'), 'right': ('2', 'right'), 'bottom': ('6', 'right')}
    cubeSides['6'] = {'map': map[150:200, 0:50], 'offset': (150, 0), 'left': ('1', 'top'), 'top': ('4', 'bottom'), 'right': ('5', 'bottom'), 'bottom': ('2', 'top')}

# traveling up/down is rows, left/right is columns
headings = [np.array([0, 1]), np.array([1, 0]), np.array([0, -1]), np.array([-1, 0])]

(currentFace, currentPoint, currentHeading) = ('1', [0, 0], 0)

for i in instructions:
    if(i.isdigit()): # walk forward
        steps = int(i)
        while(steps > 0):
            # try to take a step
            (currentRow, currentCol) = (currentPoint[0], currentPoint[1])
            (nextRow, nextCol) = (currentRow + headings[currentHeading][0], currentCol + headings[currentHeading][1])
            # determine face that the next step would be on
            if(((nextCol >= 0) & (nextRow >= 0)) & ((nextCol < maxCol) & (nextRow < maxRow))):
                (nextFace, nextPoint, nextHeading) = (currentFace, np.array([nextRow, nextCol]), currentHeading)
            elif(nextCol < 0):
                nextFace = cubeSides[currentFace]['left'][0]
                nextFaceSide = cubeSides[currentFace]['left'][1]
                (nextPoint, nextHeading) = ((np.array([maxRow - 1 - currentRow, 0]), 0) if(nextFaceSide == 'left') else
                                           (np.array([0, currentRow]), 1) if(nextFaceSide == 'top') else
                                           (np.array([currentRow, maxCol - 1]), 2) if(nextFaceSide == 'right') else
                                           (np.array([maxRow - 1, maxRow - 1 - currentRow]), 3) if(nextFaceSide == 'bottom') else None)
            elif(nextRow < 0):
                nextFace = cubeSides[currentFace]['top'][0]
                nextFaceSide = cubeSides[currentFace]['top'][1]
                (nextPoint, nextHeading) = ((np.array([currentCol, 0]), 0) if(nextFaceSide == 'left') else
                                           (np.array([0, maxCol - 1 - currentCol]), 1) if(nextFaceSide == 'top') else
                                           (np.array([maxCol - 1 - currentCol, maxCol - 1]), 2) if(nextFaceSide == 'right') else
                                           (np.array([maxRow - 1, currentCol]), 3) if(nextFaceSide == 'bottom') else None)

            elif(nextCol >= maxCol):
                nextFace = cubeSides[currentFace]['right'][0]
                nextFaceSide = cubeSides[currentFace]['right'][1]
                (nextPoint, nextHeading) = ((np.array([currentRow, 0]), 0) if(nextFaceSide == 'left') else
                                           (np.array([0, maxRow - 1 - currentRow]), 1) if(nextFaceSide == 'top') else
                                           (np.array([maxRow - 1 - currentRow, maxCol - 1]), 2) if(nextFaceSide == 'right') else
                                           (np.array([maxRow - 1, currentRow]), 3) if(nextFaceSide == 'bottom') else None)

            elif(nextRow >= maxRow):
                nextFace = cubeSides[currentFace]['bottom'][0]
                nextFaceSide = cubeSides[currentFace]['bottom'][1]
                (nextPoint, nextHeading) = ((np.array([maxCol - 1 - currentCol, 0]), 0) if(nextFaceSide == 'left') else
                                           (np.array([0, currentCol]), 1) if(nextFaceSide == 'top') else
                                           (np.array([currentCol, maxCol - 1]), 2) if(nextFaceSide == 'right') else
                                           (np.array([maxRow - 1, maxCol - 1 - currentCol]), 3) if(nextFaceSide == 'bottom') else None)

            # determine if we've hit a wall; otherwise, take step
            if(cubeSides[nextFace]['map'][nextPoint[0], nextPoint[1]] == 1):
                steps = 0
            elif(cubeSides[nextFace]['map'][nextPoint[0], nextPoint[1]] == 0):
                (currentFace, currentPoint, currentHeading) = (nextFace, nextPoint, nextHeading)
                steps -= 1
            else:
                print('a')
    else:
        if(i == 'R'):
            currentHeading = (currentHeading + 1) % 4
        elif(i == 'L'):
            currentHeading = (currentHeading - 1) % 4

projectionRow = currentPoint[0] + cubeSides[currentFace]['offset'][0] + 1
projectionCol = currentPoint[1] + cubeSides[currentFace]['offset'][1] + 1

print("Face: " + str(currentFace) + ", Row: " + str(currentPoint[0]) + ", Col: " + str(currentPoint[1]) + ", Facing: " + str(currentHeading))
print("Row: " + str(projectionRow) + ", Col: " + str(projectionCol) + ", Facing: " + str(currentHeading))
password = 1000*projectionRow + 4*projectionCol + currentHeading
print(password)
