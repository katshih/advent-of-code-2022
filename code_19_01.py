import queue
import pulp

inputFile = open("advent-of-code-2022-inputs/input_19.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

maxTime = 24
startingBots = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}
startingResources = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}
blueprints = []
for l in inputDat:
    blueprint = {}
    lSplit = l.strip().split()
    blueprint['ID'] = int(lSplit[1][:-1])
    blueprint['oreCost'] = {'ore': int(lSplit[6])}
    blueprint['clayCost'] = {'ore': int(lSplit[12])}
    blueprint['obsidianCost'] = {'ore': int(lSplit[18]), 'clay': int(lSplit[21])}
    blueprint['geodeCost'] = {'ore': int(lSplit[27]), 'obsidian': int(lSplit[30])}
    blueprints.append(blueprint)

def evaluateBlueprint(maxTime, startBots, startResources, blueprint, verbose = False):
    prob = pulp.LpProblem("blueprint", sense = pulp.LpMaximize)

    # decision variables: whether to produce each bot at each minute
    d_ore = {t: pulp.LpVariable(name=f"d_ore{t}", cat="Binary") for t in range(1, maxTime)}
    d_clay = {t: pulp.LpVariable(name=f"d_clay{t}", cat="Binary") for t in range(1, maxTime)}
    d_obsidian = {t: pulp.LpVariable(name=f"d_obsidian{t}", cat="Binary") for t in range(1, maxTime)}
    d_geode = {t: pulp.LpVariable(name=f"d_geode{t}", cat="Binary") for t in range(1, maxTime)}

    # objective function: maximize geodes
    prob += (pulp.lpSum([d_geode[t]*(maxTime - t) for t in range(1, maxTime)]), "Final Geodes")

    for t in range(1, maxTime):
        # decision constraint: only one bot per minute
        prob += (pulp.lpSum([d_ore[t], d_clay[t], d_obsidian[t], d_geode[t]]) <= 1)
        # cost constraints
        prob += (startResources['obsidian'] + pulp.lpSum([startBots['obsidian'] + pulp.lpSum([d_obsidian[k] for k in range(1, j + 1)]) for j in range(0, t - 1)])
                    - pulp.lpSum([d_geode[i]*blueprint['geodeCost']['obsidian'] for i in range(1, t + 1)]) >= 0)
        prob += (startResources['clay'] + pulp.lpSum([startBots['clay'] + pulp.lpSum([d_clay[k] for k in range(1, j + 1)]) for j in range(0, t - 1)])
                    - pulp.lpSum([d_obsidian[i]*blueprint['obsidianCost']['clay'] for i in range(1, t + 1)]) >= 0)
        prob += (startResources['ore'] + pulp.lpSum([startBots['ore'] + pulp.lpSum([d_ore[k] for k in range(1, j + 1)]) for j in range(0, t - 1)])
                    - pulp.lpSum([(d_ore[i]*blueprint['oreCost']['ore'] + d_clay[i]*blueprint['clayCost']['ore']
                                    + d_obsidian[i]*blueprint['obsidianCost']['ore'] + d_geode[i]*blueprint['geodeCost']['ore']) for i in range(1, t + 1)]) >= 0)

    status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
    if(verbose):
        print("status: " + str(pulp.LpStatus[prob.status]))
        print("objective: " + str(prob.objective.value()))
        for x in range(1, maxTime):
            robot = 'ore' if d_ore[x].varValue == 1 else ('clay' if d_clay[x].varValue == 1 else ('obsidian' if d_obsidian[x].varValue == 1 else ('geode' if d_geode[x].varValue == 1 else 'no')))
            print('Minute ' + str(x) + ': made ' + robot + ' robot')
    return prob.objective.value()

qualityTotal = 0
for blueprint in blueprints:
    geodes = evaluateBlueprint(maxTime, startingBots, startingResources, blueprint, True)
    print(geodes)
    qualityLevel = blueprint['ID']*geodes
    qualityTotal += qualityLevel

print('Quality Total: ' + str(qualityTotal))
