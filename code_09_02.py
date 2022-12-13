import numpy as np

class Rope():
    def __init__(self, init_states):
        self.nodes = [Head(init_states[0])]
        for x in init_states[1:]:
            self.nodes.append(Tail(x, self.nodes[-1]))

    def step(self, action):
        self.nodes[0].step(action)
        [x.step() for x in self.nodes[1:]]

class Head():
    def __init__(self, pos):
        self.pos = pos
        self.history = [self.pos]

    def step(self, action):
        aR_pairs = {'U': np.array([0, 1]), 'D': np.array([0, -1]), 'R': np.array([1, 0]), 'L': np.array([-1, 0])}
        self.pos = self.pos + aR_pairs[action]
        self.history.append(self.pos)

class Tail():
    def __init__(self, pos, head):
        self.pos = pos
        self.head = head
        self.history = [self.pos]

    def step(self):
        posDiff = self.head.pos - self.pos
        self.pos = self.pos + (np.linalg.norm(posDiff) > 1.5)*np.sign(posDiff)
        self.history.append(self.pos)

inputFile = open("advent-of-code-2022-inputs/input_09.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

rope = Rope([np.array([0, 0]) for x in range(10)])

for l in inputDat:
    action = l.strip().split()[0]
    number = int(l.strip().split()[1])

    for ii in range(number):
        rope.step(action)

print(len(np.unique(np.array(rope.nodes[-1].history), axis = 0)))