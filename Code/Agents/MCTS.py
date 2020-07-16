import math
import random
import time


def UCB1(v, N, n):
    try:
        return v+2*math.sqrt(math.log(N)/n)
    except ZeroDivisionError:
        return float("inf")


class MCTSNode:

    def __init__(self, gameState, children=[], parent=None):
        self.n = 0
        self.t = 0
        self.parent = parent
        self.children = children
        self.gameState = gameState

    @property
    def get_children(self):
        return self.children

    @get_children.setter
    def set_children(self, children):
        self.children = children

    def rollout(self):
        state = self.gameState
        while True:
            if state.terminal_state():
                return state.utility
            state = state.result(random.choice(state.actions))

    def backpropagate(self, value):
        self.n += 1
        self.t += value
        if self.parent:
            self.parent.backpropagate(value)

    def select(self, N):
        return max(self.children, key=lambda child: UCB1(child.t, N, child.n))

    def expand(self):
        actions = self.gameState.actions
        self.children = list(map(lambda a: self.create_child(a), actions))

    def create_child(self, action):
        return MCTSNode(self.gameState.result(action), [], self)


class MCTSTree:

    def __init__(self, initialState):
        self.initialState = initialState
        self.rootNode = MCTSNode(self.initialState, children=[], parent=None)

    def best_move(self):
        children = self.rootNode.children
        best_node = max(children, key=lambda child: child.t)
        max_index = children.index(best_node)
        print(max_index, children[max_index].t)
        return self.initialState.actions[max_index]

    def runMCTS(self):
        start_time = time.time()
        while time.time()-start_time < 3:
            current = self.rootNode
            while current.children:
                current = current.select(self.rootNode.n)
            if current.n == 0:
                value = current.rollout()
            else:
                current.expand()
                current = current.children[0]
                value = current.rollout()
            current.backpropagate(value)
        return self.best_move()
