inputFile = open("advent-of-code-2022-inputs/input_10.txt", 'r')
inputDat = inputFile.readlines()
inputFile.close()

keypoints = [20, 60, 100, 140, 180, 220]
signal = [0, 1]

for l in inputDat:
    if("noop" in l):
        signal.append(signal[-1])
    else:
        signal.append(signal[-1])
        num = int(l.strip().split()[-1])
        signal.append(signal[-1] + num)

signalStrength = [x*signal[x] for x in keypoints]
print(sum(signalStrength))

print(signal)
