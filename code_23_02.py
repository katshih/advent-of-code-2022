# with help from https://www.reddit.com/r/adventofcode/comments/zt6xz5/comment/j1f9vl0/

inputFile = open("advent-of-code-2022-inputs/input_23.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

elves = {}
for yy, l in enumerate(inputDat):
    for xx, c in enumerate(list(l.strip())):
        if(c == '#'):
            elves[(xx, len(inputDat) - 1 - yy)] = 1

#printElves(elves)
rounds = 0
directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
neighborDirections = [[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]]
currentPriority = 0
moving = True

while(moving):
    # proposals
    proposals = []
    proposedNewElves = {}
    for e in elves:
        proposal = (0, 0)

        # get neighbors
        neighborPositions = [n for n in neighborDirections if((e[0] + n[0], e[1] + n[1]) in elves)]

        # if there are neighbors, try to make a proposal
        if(len(neighborPositions) > 0):
            for priority in range(currentPriority, currentPriority + 4):
                dir = directions[priority % 4]
                idx = [i for i in dir if dir[i] != 0][0]
                if(not any([n[idx] == dir[idx] for n in neighborPositions])):
                    proposal = dir
                    break
        proposals.append(proposal)
        if((e[0] + proposal[0], e[1] + proposal[1]) in proposedNewElves):
            proposedNewElves[(e[0] + proposal[0], e[1] + proposal[1])].append((e))
        else:
            proposedNewElves[(e[0] + proposal[0], e[1] + proposal[1])] = [e]
    if(all([p == (0, 0) for p in proposals])):
        moving = False

    newElves = {}
    for coord in proposedNewElves:
        if(len(proposedNewElves[coord]) > 1):
            for x in proposedNewElves[coord]:
                newElves[x] = 1
        else:
            newElves[coord] = 1

    elves = newElves
    currentPriority = (currentPriority + 1) % 4
    rounds += 1
    print(rounds)

print('Total Rounds: ' + str(rounds))
