import math
import random
import time
from copy import deepcopy


def UCB1(v, N, n):
    try:
        return v/n+2*math.sqrt(2*math.log(N)/n)
    except ZeroDivisionError:
        return float("inf")
    except ValueError:
        return float("inf")


class MCTSNode:

    def __init__(self, state, children=[], parent=None):
        self.n = 0
        self.t = 0
        self.parent = parent
        self.children = children
        self.state = state

    @property
    def get_children(self):
        return self.children

    @get_children.setter
    def set_children(self, children):
        self.children = children

    def rollout(self):
        state = deepcopy(self.state)
        while True:
            if state.terminal_state():
                return state.utility2(1)
            state = state.result(random.choice(state.actions))

    def backpropagate(self, value):
        self.n += 1
        self.t += value
        if self.parent:
            self.parent.backpropagate(value)

    def select(self):
        return max(self.children, key=lambda child: UCB1(child.t, self.n, child.n))

    def expand(self):
        actions = deepcopy(self.state.actions)
        self.children = [self.create_child(a) for a in actions]
        return self.children[0]

    def create_child(self, action):
        return MCTSNode(self.state.result(action), [], self)


class MCTSTree:

    def __init__(self, initialState):
        self.initialState = initialState
        self.rootNode = MCTSNode(self.initialState, children=[], parent=None)

    def best_move(self):
        children = self.rootNode.children
        best_node = max(children, key=lambda child: child.t/child.n)
        max_index = children.index(best_node)
        return self.initialState.actions[max_index]

    def runMCTS(self, max_time=3):
        start_time = time.time()
        while time.time()-start_time < max_time:
            current = self.rootNode
            while not current.state.terminal_state():
                if not current.children:
                    current = current.expand()
                    break
                else:
                    current = current.select()
            value = current.rollout()
            current.backpropagate(value)
        return self.best_move()
