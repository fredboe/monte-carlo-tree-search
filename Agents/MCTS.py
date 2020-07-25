import math
import random
import time
from copy import deepcopy


def UCB1(v, N, n):
    """
        Parameters:
                    v: int -> value of the terminal_state
                    N: int -> number of times the parent node was visited
                    n: int -> number of times the node was visited
        returns:
                int for MCTS selection
    """
    try:
        # UCB1 formula
        return v/n+2*math.sqrt(2*math.log(N)/n)
    except ZeroDivisionError:
        # if n is zero return infinity -> this node needs to be expanded
        return float("inf")
    except ValueError:
        # if n is not set return infinity -> this node needs to be expanded
        return float("inf")


class MCTSNode:

    def __init__(self, state, children=[], parent=None):
        # number of times the node was visited
        self.n = 0
        # total value
        self.t = 0
        # parent object (MCTSNode)
        self.parent = parent
        # list of children (MCTSNodes)
        self.children = children
        # GameState of the node
        self.state = state

    @property
    def get_children(self):
        """
            returns children (list)
        """
        return self.children

    @get_children.setter
    def set_children(self, children):
        """
            sets children (list)
        """
        self.children = children

    def rollout(self, player_id):
        """
            Parameters:
                        player_id: int (1 or 2)
            simulates the game randomly
            -> returns:
                        utility (value) of the terminal_state
        """
        state = deepcopy(self.state)
        while True:
            if state.terminal_state():
                return state.utility2(player_id)
            state = state.result(random.choice(state.actions))

    def backpropagate(self, value):
        """
            Parameters:
                        value: int (1 or -1)
            adds value to the total value (self.t) and increases self.n by 1
            then if the MCTSNode has a parent execute backpropagation with the parent
            -> executes backpropagate for all visited nodes of the rollout
        """
        self.n += 1
        self.t += value
        if self.parent:
            self.parent.backpropagate(value)

    def select(self):
        """
            returns:
                    the child with the maximum UCB1-score of all children
        """
        return max(self.children, key=lambda child: UCB1(child.t, self.n, child.n))

    def expand(self):
        """
            returns:
                    the first children of the expanded children
            fills self.children with new MCTSNodes
        """
        actions = deepcopy(self.state.actions)
        self.children = [self.create_child(a) for a in actions]
        return self.children[0]

    def create_child(self, action):
        """
            Parameters:
                        action: int
            returns:
                    MCTSNode of the action's result
        """
        return MCTSNode(self.state.result(action), [], self)


class MCTSTree:

    def __init__(self, initialState):
        # initial GameState
        self.initialState = initialState
        # creates root node: MCTSNode
        self.rootNode = MCTSNode(self.initialState, children=[], parent=None)

    def best_move(self):
        """
            returns:
                    the best move of children (action: int)
                    that maximises its total score divided by its
                    total number of visits
        """
        children = self.rootNode.children
        best_node = max(children, key=lambda child: child.t/child.n)
        max_index = children.index(best_node)
        return self.initialState.actions[max_index]

    def runMCTS(self, player_id, max_time=5):
        """
            Parameters:
                        player_id: int (1 or 2)
                        max_time: float (number of seconds the algorithm should run)
            returns:
                    best_move()
            executes the MCTS algorithm
            -> FIRST: find root node
            -> SECOND: select child that should be visited next
            -> THIRD: simulate the game from the current (root node) on (rollout)
            -> FOURTH: propagate backwards (backpropagate) for all visited nodes
                       in that game run
            -> FIFTH: select the best founded move and return it (action)
        """
        start_time = time.time()
        while time.time()-start_time < max_time:
            current = self.rootNode
            while not current.state.terminal_state():
                if not current.children:
                    current = current.expand()
                    break
                else:
                    current = current.select()
            value = current.rollout(player_id)
            current.backpropagate(value)
        return self.best_move()
