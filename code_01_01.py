inputFile = open("input/input_01.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

maxCal = 0
elf = 0

for l in inputDat:
    if(l.strip()):
         elf = elf + int(l)
    else:
         if(elf >= maxCal):
             maxCal = elf
         elf = 0
if(elf >= maxCal):
    maxCal = elf

print(maxCal)