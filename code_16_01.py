inputFile = open("advent-of-code-2022-inputs/input_16_test.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

valveDict = {}

for l in inputDat:
    valveName = l.split()[1]
    flowRate = int(l.split('=')[1].split(';')[0])
    neighborList = l.split('valve')[1].strip('s').split()
    neighbors = {}
    for n in neighborList:
        neighbors[n.strip(',')] = 1
    valveDict[valveName] = {'f': flowRate, 'n': neighbors, 'o': False}

print("Total: " + str(len(valveDict)))
print("Zeros: " + str(len([v for v in valveDict if valveDict[v]['f'] == 0])))

# remove valves with zero flow rate and create weighted graph
delList = []
for v in valveDict:
    if((valveDict[v]['f'] == 0)):
        for n in valveDict[v]['n']:
            nVal = valveDict[v]['n'][n]
            for nR in valveDict[v]['n']:
                if(nR != n):
                    totalPath = nVal + valveDict[v]['n'][nR]
                    if(n in valveDict[nR]['n']):
                        if((totalPath < valveDict[nR]['n'][n])):
                            valveDict[nR]['n'][n] = totalPath
                    else:
                        valveDict[nR]['n'][n] = totalPath
    if((v != 'AA') & (valveDict[v]['f'] == 0)):
        for v2 in valveDict:
            if(v in valveDict[v2]['n']):
                valveDict[v2]['n'].pop(v)
        delList.append(v)
for v in delList:
    valveDict.pop(v)
print("Total Remaining: " + str(len(valveDict)))

# get min distances between all nodes remaining
calculatedNodes = []
for v in valveDict:
    calculatedNodes.append(v)
    calcDict = {k: valveDict[k] for k in valveDict if k not in calculatedNodes}
