inputFile = open("advent-of-code-2022-inputs/input_21.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

class Monkey():
    def __init__(self, jobType, number = None, parents = [None, None]):
        self.jobType = jobType
        self.number = number
        self.parents = parents

    def getNumber(self, tribe):
        if(self.number is not None):
            return self.number
        else:
            if(self.jobType == '+'):
                self.number = tribe[self.parents[0]].getNumber(tribe) + tribe[self.parents[1]].getNumber(tribe)
            elif(self.jobType == '-'):
                self.number = tribe[self.parents[0]].getNumber(tribe) - tribe[self.parents[1]].getNumber(tribe)
            elif(self.jobType == '*'):
                self.number = tribe[self.parents[0]].getNumber(tribe)*tribe[self.parents[1]].getNumber(tribe)
            else:
                self.number = tribe[self.parents[0]].getNumber(tribe)/tribe[self.parents[1]].getNumber(tribe)

        return self.number

tribe = {}

for l in inputDat:
    splitString = l.strip().split()
    name = splitString[0][0:-1]
    #print('Monkey name: ' + splitString[0][0:-1])
    if(splitString[1].isdigit()):
        #print('number: ' + splitString[1])
        tribe[name] = Monkey('number', number = int(splitString[1]))
    else:
        #print('operation: ' + splitString[2] + ', parents: ' + splitString[1] + ', ' + splitString[3])
        tribe[name] = Monkey(splitString[2], parents = [splitString[1], splitString[3]])

print(tribe['root'].getNumber(tribe))
