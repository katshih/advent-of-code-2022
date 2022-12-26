import numpy as np

inputFile = open("advent-of-code-2022-inputs/input_23.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

elves = []
for yy, l in enumerate(inputDat):
    for xx, c in enumerate(list(l.strip())):
        if(c == '#'):
            elves.append(np.array([xx, len(inputDat) - 1 - yy]))

def printElves(elves):
    (minX, maxX, minY, maxY) = (min([e[0] for e in elves]),
                                max([e[0] for e in elves]),
                                min([e[1] for e in elves]),
                                max([e[1] for e in elves]))
    offset = np.array([minX, minY])
    ground = [['.' for x in range(minX, maxX + 1)] for y in range(minY, maxY + 1)]
    strList = []
    for yy, lin in enumerate(ground):
        str = ''
        for xx, c in enumerate(lin):
            str = str + '#' if(any((e  - offset == np.array([xx, yy])).all() for e in elves)) else str + '.'
        strList.append(str)
    for str in strList[-1::-1]:
        print(str)
    print('\n')

#printElves(elves)
rounds = 10
directions = np.array([[0, 1], [0, -1], [-1, 0], [1, 0]])
neighborDirections = np.array([[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]])
currentPriority = 0
for r in range(0, rounds):
    print(r + 1)
    # proposals
    proposals = []
    for e in elves:
        proposal = np.array([0, 0])
        # get neighbors
        neighborPositions = [n for n in neighborDirections if(any((e + n == x).all() for x in elves))]
        #print(neighborPositions)
        # if there are neighbors, try to make a proposal
        if(len(neighborPositions) > 0):
            for priority in range(currentPriority, currentPriority + 4):
                dir = directions[priority % 4]
                #print(dir)
                idx = [i for i in dir if dir[i] != 0][0]
                #print(idx)
                #[print(n[idx] == dir[idx]) for n in neighborPositions]
                if(not any([n[idx] == dir[idx] for n in neighborPositions])):
                    proposal = dir
                    break
        #print(e)
        #print(proposal)
        proposals.append(proposal)
    # moves
    proposedNewElves = [e + p for (e, p) in zip(elves, proposals)]
    newElves = []
    for e, p in zip(elves, proposals):
        if((p == np.array([0, 0])).all()):
            newElves.append(e)
        else:
            move = len([x for x in proposedNewElves if((e + p == x).all())]) == 1
            newElves.append(e + move*p)

    currentPriority = (currentPriority + 1) % 4
    elves = newElves
    #printElves(elves)
(minX, maxX, minY, maxY) = (min([e[0] for e in elves]),
                            max([e[0] for e in elves]),
                            min([e[1] for e in elves]),
                            max([e[1] for e in elves]))

rectangle = (maxX - minX + 1)*(maxY - minY + 1)
emptyGround = rectangle - len(elves)
print(emptyGround)
