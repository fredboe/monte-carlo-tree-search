import math
import random
import time
from copy import deepcopy


def UCB1(v, N, n):
    try:
        return v+math.sqrt(5*math.log(N)/n)+(5*(v/n))/(n+1)
    except ZeroDivisionError:
        return float("inf")
    except ValueError:
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
        state = deepcopy(self.gameState)
        while True:
            if state.terminal_state():
                return state.utility2(1)
            state = state.result(random.choice(state.actions))

    def backpropagate(self, value):
        self.n += 1
        self.t += value
        if self.parent:
            self.parent.backpropagate(value)

    def select(self, N):
        return max(self.children, key=lambda child: UCB1(child.t, N, child.n))

    def expand(self):
        actions = deepcopy(self.gameState.actions)
        self.children = [self.create_child(a) for a in actions]

    def create_child(self, action):
        return MCTSNode(self.gameState.result(action), [], self)


class MCTSTree:

    def __init__(self, initialState):
        self.initialState = initialState
        self.rootNode = MCTSNode(self.initialState, children=[], parent=None)
        self.rootNode.expand()

    def best_move(self):
        children = self.rootNode.children
        best_node = max(children, key=lambda child: child.t)
        max_index = children.index(best_node)
        return self.initialState.actions[max_index]

    def runMCTS(self):
        state=self.rootNode.gameState
        for action in state.actions:
            new_state = state.result(action)
            if new_state.terminal_state() and new_state.winner:
                return action
        start_time = time.time()
        while time.time()-start_time < 2:
            current = self.rootNode
            while current.children:
                current = current.select(self.rootNode.n)
            if current.gameState.terminal_state():
                self.rootNode.n += 1
                continue
            counter+=1
            if current.n == 0:
                value = current.rollout()
            else:
                current.expand()
                current = current.children[0]
                value = current.rollout()
            current.backpropagate(value)
        return self.best_move()
