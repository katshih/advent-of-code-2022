inputFileCrates = open("input/input_05_01.txt", "r")
inputDatCrates = inputFileCrates.readlines()
inputFileCrates.close()

nCols = max([int(x) for x in inputDatCrates[-1].split()])
crates = []
[crates.append([]) for ii in range(0, nCols)]

a = [(list(x[1:-1:4])) for x in inputDatCrates[0:-1]]
for l in reversed(a):
    for ii in range(0, nCols):
        if(l[ii].strip()): crates[ii].append(l[ii])

inputFileMoves = open("input/input_05_02.txt", "r")
inputDatMoves = inputFileMoves.readlines()
inputFileMoves.close()

for l in inputDatMoves:
    parse = [int(x) for x in l.split()[1::2]]
    c = crates[parse[1] - 1][-parse[0]:]
    crates[parse[1] - 1][-parse[0]:] = []
    [crates[parse[2] - 1].append(x) for x in c]

[print(x[-1]) for x in crates]