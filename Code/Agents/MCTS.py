import math
import random
import time
from copy import deepcopy


def UCB1(v, N, n):
    #print(type(v),type(N),type(n))
    try:
        return v+math.sqrt(25*math.log(N)/n)+(25*(v/n))/(n+1)
    except ZeroDivisionError:
        return float("inf")
    except ValueError:
        return float("inf")

def average(v,n):
    try:
        return v/n
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
        state = deepcopy(self.gameState)
        while True:
            if state.terminal_state():
                return state.utility2(1)
            state = state.result(random.choice(state.actions))

    def backpropagate(self, value):
        self.n += 1
        self.t += value
        #print(self.gameState)
        if self.parent:
            self.parent.backpropagate(value)

    def select(self, N):
        #print([child.n for child in self.children])
        #print(self.children)
        #print()
        #print(self.children)
        #print([UCB1(child.t, N, child.n) for child in self.children])
        #print(self.children.index(max(self.children, key=lambda child: UCB1(child.t, N, child.n))))
        #return max(self.children, key=lambda child: average(child.t, child.n))
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

    def backpropagate(self, current, value):
        current.n += 1
        current.t += value
        print(current.gameState)
        if current.parent:
            self.backpropagate(current.parent, value)

    def runMCTS(self):
        counter = 0
        #print(self.rootNode)
        state=self.rootNode.gameState
        for action in state.actions:
            new_state = state.result(action)
            if new_state.terminal_state() and new_state.winner:
                return action
        start_time = time.time()
        while time.time()-start_time < 2:
        #while counter <10:
            current = self.rootNode
            while current.children:
                #print("LEAF")
                current = current.select(self.rootNode.n)
            #print(current.n)
            #print(current.gameState)
            if current.gameState.terminal_state():
                #print(current.gameState)
                #current.backpropagate(1)
                self.rootNode.n += 1
                continue
            counter+=1
            if current.n == 0:
                #print("N=0")
                value = current.rollout()
            else:
                #print("N is not 0")
                current.expand()
                current = current.children[0]
                value = current.rollout()
            current.backpropagate(value)
        """try:
            print(self.rootNode.children[0].t, self.rootNode.children[1].t)
        except Exception:
            print("failed")"""
        print(counter)
        return self.best_move()
