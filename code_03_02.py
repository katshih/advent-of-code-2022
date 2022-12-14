def get_priority(item):
    ascii = ord(item)
    if(ascii > 90):
        priority = ascii - 96
    else:
        priority = ascii - 38
    return priority

inputFile = open("advent-of-code-2022-inputs/input_03.txt", 'r')
inputData = inputFile.readlines()

sum = 0
group = []
for l in inputData:
    group.append(l.strip())
    if(len(group) == 3):
        dupe = set(group[0]).intersection(set(group[1])).intersection(set(group[2]))
        sum = sum + get_priority(list(dupe)[0])
        group = []
print(sum)
