inputFile = open("advent-of-code-2022-inputs/input_25.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

def SNAFUToDec(snafu):
    dec = 0
    for place, digit in enumerate(list(snafu)[-1::-1]):
        if(digit == '-'): digit = -1
        elif(digit == '='): digit = -2
        dec += int(digit)*5**place
    return dec

def decToSNAFU(dec):
    snafuDefs = {0: '0', 1: '1', 2: '2', 4: '-', 3:'='}
    snafu = ''
    while(dec > 0):
        remainder = dec % 5
        digit = snafuDefs[remainder]
        snafu += digit
        dec -= (remainder if remainder <= 2 else -5 + remainder)
        dec /= 5
    snafu = snafu[-1::-1]
    return snafu

sum = 0
for l in inputDat:
    sum += SNAFUToDec(l.strip())

decToSNAFU(sum)
print(sum)
print(decToSNAFU(sum))
