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

all_dists = dict(nx.algorithms.shortest_paths.weighted.all_pairs_dijkstra(tunnelGraph))
startNode = "AA"
maxTime = 30
startReward = 0

# greedy algorithm to get a lower bound
def greedy(timeRemaining, currentReward, currentNode, validNodes, currentRoute):
    while(timeRemaining):
        rewards = [(n, 
                    tunnelGraph.nodes[n]["flow"]*(timeRemaining - 1 - all_dists[currentNode][0][n]),
                    1 + all_dists[currentNode][0][n])
                    for n in validNodes]
        best = max(rewards, key = lambda x: x[1])
        if(best[1] > 0):
            currentRoute.append(best[0])
            currentNode = best[0]
            validNodes.remove(best[0])
            currentReward += best[1]
            timeRemaining -= best[2]
        else:
            break
    return(currentReward, currentRoute)

def upperBound(timeRemaining, currentReward, currentNode, validNodes):
    # traveling to each node at once gives an upper bound
    rewards = [tunnelGraph.nodes[n]["flow"]*(timeRemaining - 1 - all_dists[currentNode][0][n]) for n in validNodes]
    for r in rewards:
        if(r > 0):
            currentReward += r
    return currentReward

(bestReward, bestRoute) = greedy(maxTime, startReward, startNode, list(tunnelGraph.nodes), [startNode])
print("Greedy: " + str(bestReward) + ", " + str(bestRoute))
nodeQueue = queue.Queue()
# queue stores branches as: (time remaining, reward total, path, nodes remaining)
 
[nodeQueue.put((maxTime - 1 - all_dists[startNode][0][node],
                tunnelGraph.nodes[node]["flow"]*(maxTime - 1 - all_dists[startNode][0][node]), 
                [startNode, node], 
                [n for n in list(tunnelGraph.nodes) if((n != node) & (n != startNode))]))
                for node in tunnelGraph.nodes if (node != startNode)]

while(not nodeQueue.empty()):
    (timeLeft, rewardTotal, path, validNodes) = nodeQueue.get()
    # check the upper bound given that this path is followed
    branchBest = upperBound(timeLeft, rewardTotal, path[-1], validNodes)
    if(branchBest == rewardTotal): # if there's no way to get a reward
        if(branchBest > bestReward):
            bestReward = branchBest
            print(bestReward)
            print(path)
            bestRoute = path
    if(branchBest > bestReward): # possible better solution
        for node in validNodes: # move to each node and put path in queue
            timeRequired = 1 + all_dists[path[-1]][0][node]
            reward = tunnelGraph.nodes[node]["flow"]*(timeLeft - timeRequired)
            nodeQueue.put((timeLeft - timeRequired, rewardTotal + reward, path + [node], [n for n in validNodes if(n != node)]))
print(bestReward)
print(bestRoute)