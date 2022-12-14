inputFile = open("advent-of-code-2022-inputs/input_10.txt", 'r')
inputDat = inputFile.readlines()
inputFile.close()

signal = [0, 1]
row_size = 40

for l in inputDat:
    if("noop" in l):
        signal.append(signal[-1])
    elif("addx" in l):
        signal.append(signal[-1])
        num = int(l.strip().split()[-1])
        signal.append(signal[-1] + num)

for ii, s in enumerate(signal[1:]):
    CRT_px = ii % 40
    px_val = '#' if (abs(s - CRT_px) <= 1) else '.'
    endline = '\n' if CRT_px == 39 else ''
    print(px_val, end = endline)
