inputFile = open("input/input_01.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

maxCal = [0, 0, 0]
elf = 0

for l in inputDat:
    if(l.strip()):
        elf = elf + int(l)
    else:
        if(elf >= min(maxCal)):
            argmin = maxCal.index(min(maxCal))
            maxCal[argmin] = elf
        elf = 0

print(sum(maxCal))