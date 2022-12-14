inputFile = open("advent-of-code-2022-inputs/input_11.txt", 'r')
inputDat = inputFile.readlines()
inputFile.close()

class Monkey():
    def __init__(self, items, worryFunc, testFunc, trueMonkey, falseMonkey):
        self.items = items
        self.updateWorry = worryFunc
        self.testWorry = testFunc
        self.trueMonkey = trueMonkey
        self.falseMonkey = falseMonkey
        self.inspections = 0

    def takeTurn(self, troop, verbose = False):
        for i in self.items:
            self.inspections += 1
            worry = int(self.updateWorry(i)/3)
            monkeyTarget = self.trueMonkey if(self.testWorry(worry)) else self.falseMonkey
            troop[monkeyTarget].items.append(worry)
            if(verbose):
                print("initial: " + str(i) + ", inspected: " + str(self.updateWorry(i)) + ", final: " + str(worry))
                print("test is " + str(self.testWorry(worry)))
                print("throwing to monkey " + monkeyTarget)

        self.items = []

(monkeyName, monkeyItems, monkeyWorryFunc, monkeyTestFunc, monkeyTrue, monkeyFalse) = (None, None, None, None, None, None)
monkeys = {}

for l in inputDat:
    lineType = l.strip().split()
    if("Monkey" in lineType):
        monkeyName = l.strip().replace(':', '').split()[1]
    elif("Starting" in lineType):
        monkeyItems = [int(x) for x in list(l.strip().split(':')[1].split(','))]
    elif("Operation:" in lineType):
        equation = list(l.strip().split('=')[1].strip().split())
        if(equation[2] == 'old'):
            monkeyWorryFunc = lambda x : (x*x)
        elif(equation[1] == '+'):
            monkeyWorryFunc = lambda x, add = int(equation[2]): (x + add)
        elif(equation[1] == '*'):
            monkeyWorryFunc = lambda x, mult = int(equation[2]): (x*mult)
    elif("Test:" in lineType):
        monkeyTestFunc = lambda x, divisor = int(l.strip().split()[-1]): (x % divisor == 0)
    elif("true:" in lineType):
        monkeyTrue = l.strip().split()[-1]
    elif("false:" in lineType):
        monkeyFalse = l.strip().split()[-1]

    if(monkeyFalse is not None):
        monkeys[monkeyName] = Monkey(monkeyItems, monkeyWorryFunc, monkeyTestFunc, monkeyTrue, monkeyFalse)
        (monkeyName, monkeyItems, monkeyWorryFunc, monkeyTestFunc, monkeyTrue, monkeyFalse) = (None, None, None, None, None, None)

numRounds = 20

for round in range(numRounds):
    for key in monkeys:
        monkeys[key].takeTurn(monkeys)

inspectList = [monkeys[key].inspections for key in monkeys]
inspectList.sort(reverse = True)
print(inspectList[0]*inspectList[1])
