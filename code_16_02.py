# the team orienteering problem with decreasing profits and no fixed endpoint

import networkx as nx
import queue

inputFile = open("advent-of-code-2022-inputs/input_16.txt", "r")
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
    valveDict[valveName] = {'f': flowRate, 'n': neighbors, 'c': True}

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

tunnelGraph = nx.Graph()
for v in valveDict:
    for n in valveDict[v]['n']:
        tunnelGraph.add_edge(v, n, weight = valveDict[v]['n'][n])
    tunnelGraph.add_node(v, flow=valveDict[v]['f'], closed=valveDict[v]['c'])

print(len(valveDict))

all_dists = dict(nx.algorithms.shortest_paths.weighted.all_pairs_dijkstra(tunnelGraph))
startNode = "AA"
maxTime = 26
startReward = 0

# greedy algorithm to get a lower bound
def greedy(timeRemainingH, timeRemainingE, currentReward, currentNodeH, currentNodeE, validNodes, currentRoute):
    while(timeRemainingH or timeRemainingE):
        rewardsH = [(n, 
                    tunnelGraph.nodes[n]["flow"]*(timeRemainingH - 1 - all_dists[currentNodeH][0][n]),
                    1 + all_dists[currentNodeH][0][n])
                    for n in validNodes]
        rewardsE = [(n, 
                    tunnelGraph.nodes[n]["flow"]*(timeRemainingE - 1 - all_dists[currentNodeE][0][n]),
                    1 + all_dists[currentNodeE][0][n])
                    for n in validNodes]
        bestH = max(rewardsH, key = lambda x: x[1])
        bestE = max(rewardsE, key = lambda x: x[1])
        if((bestH[1] >= bestE[1]) & (bestH[1] > 0)):
            currentRoute.append(bestH[0])
            currentNodeH = bestH[0]
            validNodes.remove(bestH[0])
            currentReward += bestH[1]
            timeRemainingH -= bestH[2]
        elif((bestE[1] > 0)):
            currentRoute.append(bestE[0])
            currentNodeE = bestE[0]
            validNodes.remove(bestE[0])
            currentReward += bestE[1]
            timeRemainingE -= bestE[2]
        else:
            break
    return(currentReward, currentRoute)

def upperBound(timeRemainingH, timeRemainingE, currentReward, currentNodeH, currentNodeE, validNodes):
    # traveling to each node at once gives an upper bound
    rewardsE = [tunnelGraph.nodes[n]["flow"]*(timeRemainingE - 1 - all_dists[currentNodeE][0][n]) for n in validNodes]
    rewardsH = [tunnelGraph.nodes[n]["flow"]*(timeRemainingH - 1 - all_dists[currentNodeH][0][n]) for n in validNodes]
    for rE, rH in zip(rewardsE, rewardsH):
        if(max(rE, rH) > 0):
            currentReward += max(rE, rH)
    return currentReward

(bestReward, bestRoute) = greedy(maxTime, maxTime, startReward, startNode, startNode, list(tunnelGraph.nodes), [startNode])
print("Greedy: " + str(bestReward) + ", " + str(bestRoute))
print("Upper: " + str(upperBound(maxTime, maxTime, startReward, startNode, startNode, list(tunnelGraph.nodes))))
nodeQueue = queue.LifoQueue()
# queue stores branches as: (time remaining E, time remainin H, reward total, path, nodes remaining)
 
[nodeQueue.put((maxTime - 1 - all_dists[startNode][0][node],
                maxTime,
                tunnelGraph.nodes[node]["flow"]*(maxTime - 1 - all_dists[startNode][0][node]), 
                [startNode, node], 
                [startNode],
                [n for n in list(tunnelGraph.nodes) if((n != node) & (n != startNode))]))
                for node in tunnelGraph.nodes if (node != startNode)]

while(not nodeQueue.empty()):
    (timeLeftH, timeLeftE, rewardTotal, pathH, pathE, validNodes) = nodeQueue.get()
    # check the upper bound given that this path is followed
    branchBest = upperBound(timeLeftH, timeLeftE, rewardTotal, pathH[-1], pathE[-1], validNodes)
    if(branchBest == rewardTotal): # if there's no way to get a reward
        if(branchBest > bestReward):
            bestReward = branchBest
            print(bestReward)
            print("Human: " + str(pathH) + ", Elephant: " + str(pathE))
    if(branchBest > bestReward): # possible better solution
        for node in validNodes: # move to each node and put path in queue
            timeRequiredH = 1 + all_dists[pathH[-1]][0][node]
            reward = tunnelGraph.nodes[node]["flow"]*(timeLeftH - timeRequiredH)
            if(reward > 0):
                nodeQueue.put((timeLeftH - timeRequiredH, timeLeftE, rewardTotal + reward, pathH + [node], pathE, [n for n in validNodes if(n != node)]))
            # if elephant moves there
            timeRequiredE = 1 + all_dists[pathE[-1]][0][node]
            reward = tunnelGraph.nodes[node]["flow"]*(timeLeftE - timeRequiredE)
            if(reward > 0):
                nodeQueue.put((timeLeftH, timeLeftE - timeRequiredE, rewardTotal + reward, pathH, pathE + [node], [n for n in validNodes if(n != node)]))
print(bestReward)
#print(bestRoute)