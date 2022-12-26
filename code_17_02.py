inputFile = open("advent-of-code-2022-inputs/input_17.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

chamberWidth = 7
rockStart = [3, 2]

rockTypes = [[[0, 0], [0, 1], [0, 2], [0, 3]],
             [[0, 1], [1, 0], [1, 1], [1, 2], [2, 1]],
             [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]],
             [[0, 0], [1, 0], [2, 0], [3, 0]],
             [[0, 0], [0, 1], [1, 0], [1, 1]]]

jetPattern = list(inputDat[0].strip())
jetPattern = [-1 if x == '<' else 1 for x in jetPattern]
jetLength = len(jetPattern)
grid = [[1 for x in range(chamberWidth + 2)]]
jetIdx = 0
totalHeight = 0
height = 0

memory = 20
cycles = 0
checkpoints = []

totalRocks = 1000000000000
rockNum = 0
flag = 0

def printGridWithRock(grid, rockLoc, rockIdx):
    pieceLocs = []
    for piece in rockTypes[rockIdx]:
        pieceLocs.append([rockLoc[0] + piece[0], rockLoc[1] + piece[1]])
    for row, line in enumerate(grid[-1::-1]):
        for col, point in enumerate(line):
            print('@', end='') if [len(grid) - 1  - row, col] in pieceLocs else print('.', end='') if point == 0 else print('#', end='')
        print('\r')
    print('\n')

def printGrid(grid):
    for line in grid[-1::-1]:
        for point in line:
            print('.', end='') if point == 0 else print('#', end='')
        print('\r')
    print('\n')

while(rockNum < totalRocks):
    if(len(grid) <= height + rockStart[0] + 4):
        [grid.append([1] + [0 for x in range(chamberWidth)] + [1]) for c in range(height + rockStart[0] + 5 - len(grid))]
    (rockIdx, rockLoc, rockStopped) = (rockNum % len(rockTypes), [height + rockStart[0] + 1, rockStart[1] + 1], False)
    #printGridWithRock(grid, rockLoc, rockIdx)
    while(not rockStopped):
        rockLoc = [rockLoc[0], rockLoc[1] + jetPattern[jetIdx]]
        for piece in rockTypes[rockIdx]:
            pieceLoc = [rockLoc[0] + piece[0], rockLoc[1] + piece[1]]
            if(grid[pieceLoc[0]][pieceLoc[1]] != 0):
                rockLoc = [rockLoc[0], rockLoc[1] - jetPattern[jetIdx]]
                break
        #printGridWithRock(grid, rockLoc, rockIdx)
        rockLoc = [rockLoc[0] - 1, rockLoc[1]]
        for piece in rockTypes[rockIdx]:
            pieceLoc = [rockLoc[0] + piece[0], rockLoc[1] + piece[1]]
            if(grid[pieceLoc[0]][pieceLoc[1]] != 0):
                rockLoc = [rockLoc[0] + 1, rockLoc[1]]
                rockStopped = True
                maxPiece = 0
                for piece in rockTypes[rockIdx]:
                    pieceLoc = [rockLoc[0] + piece[0], rockLoc[1] + piece[1]]
                    maxPiece = max(maxPiece, pieceLoc[0])
                    grid[pieceLoc[0]][pieceLoc[1]] = 1
                height = max(height, maxPiece)
                break
        #printGrid(grid) if rockStopped else printGridWithRock(grid, rockLoc, rockIdx)
        jetIdx = (jetIdx + 1) % jetLength

    point = [grid[height - memory:height + 1], jetIdx, rockIdx]
    if(point in checkpoints):
        if(flag == 0):
            print('Height: ' + str(height))
            print('Rock: ' + str(rockNum))
            baseHeight = height
            baseNum = rockNum
            flag = 1
        elif(flag == 1):
            cycleHeight = height - baseHeight
            cycleRocks = rockNum - baseNum
            numCycles = int((totalRocks - baseNum)/cycleRocks)
            rockNum += cycleRocks*(numCycles - 1)
            print('Cycle Height: ' + str(cycleHeight))
            print('Rocks in Cycle: ' + str(cycleRocks))
            print('Total Cycles: ' + str(numCycles))
            print('Skipping from rock #' + str(rockNum - cycleRocks*(numCycles - 1)) + ' to rock #' + str(rockNum))
            grid = grid[height - memory:]
            height = memory
        checkpoints = []
    checkpoints.append(point)
    rockNum += 1

totalHeight = baseHeight + cycleHeight*numCycles + height - memory
print(totalHeight)
