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
for l in inputData:
    comp_1 = set(list(l[0:int((len(l) - 1)/2)]))
    comp_2 = set(list(l[int((len(l) - 1)/2):-1]))
    dupe = comp_1.intersection(comp_2)
    sum = sum + get_priority(list(dupe)[0])

print(sum)
