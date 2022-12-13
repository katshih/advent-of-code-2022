def getScore(opponent, player):
    shapeScores = {'X': 1, 'Y': 2, 'Z': 3}
    oppScores = {'A': 1, 'B': 2, 'C': 3}
    gameScores = {0: 3, 1: 6, 2: 0}
    # 0 is draw, 1 is win, 2 is lose
    game = (shapeScores[player] - oppScores[opponent]) % 3

    return(shapeScores[player] + gameScores[game])

inputFile = open("advent-of-code-2022-inputs/input_02.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

score = 0
for l in inputDat:
    score = score + getScore(l[0], l[2])

print(score)