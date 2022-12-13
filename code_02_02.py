def getScore(opponent, strategy):
    stratScores = {'X': 0, 'Y': 3, 'Z': 6}
    shapeScores = {'A': 1, 'B': 2, 'C': 3}
    rel = (shapeScores[opponent] + (int(stratScores[strategy]/3) - 1)) % 3
    if(rel == 0): rel = 3

    return(stratScores[strategy] + rel)

inputFile = open("advent-of-code-2022-inputs/input_02.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

score = 0
for l in inputDat:
    getScore(l[0], l[2])
    score = score + getScore(l[0], l[2])

print(score)