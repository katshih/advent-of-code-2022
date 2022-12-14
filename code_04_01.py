import re

inputFile = open("advent-of-code-2022-inputs/input_04.txt", 'r')
inputData = inputFile.readlines()

sum = 0
for l in inputData:
    list = [int(x) for x in re.split(',|-', l.strip())]
    sum = sum + (((list[0] >= list[2]) & (list[1] <= list[3])) | ((list[2] >= list[0]) & (list[3] <= list[1])))

print(sum)
