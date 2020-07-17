# from collections import namedtuple
import sys
from Game.GameStateConnect4 import GameState
from Agents.MCTS import MCTSTree
from Agents.Random import RandomAgent
from Agents.AlphaBeta import AlphaBetaAgent


"""Games = namedtuple("Games", "Connect4")
games = Games(GameState)"""

start_board_list = ["000000 " for i in range(0, 7)]
start_board = "".join(start_board_list)


class Match:

    def __init__(self, agents, start_board):
        self.agent_player, self.agent_opponent = agents
        self.start_board = start_board
        self.initialState = GameState(start_board, 1)
        self.run_Match(self.initialState)

    def get_action_from_agent_MCTS(self, state):
        return MCTSTree(state).runMCTS()

    def get_action_from_agent_RANDOM(self, state):
        return RandomAgent().get_action(state)

    def get_action_from_agent_ALPHABETA(self, state):
        return AlphaBetaAgent().get_action(state)

    def run_Match(self, state):
        while not state.terminal_state():
            if state.player_id == 1:
                action = self.get_action_from_agent_MCTS(state)
                print("MCTS plays action: "+str(action))
            else:
                print("ALPHABETA plays action: "+str(action))
                action = self.get_action_from_agent_ALPHABETA(state)
            if action not in state.actions:
                print("\n\nSorry, but this action isn't AVAILABLE.\n\n")
                continue
            state = state.result(action)
            print(str(state))
        winner = state.winner
        print("Player "+str(winner)+" has won." if winner else "Nobody won!")

    def get_action_from_REALWORLD(self):
        int_input = False
        action = None
        while not int_input:
            try:
                action = int(input("Please type in your action. "
                                   + "It has to be a number between 1 and 8."
                                   + "Type in 0 to stop the game!"))
                if action == 0:
                    print("\nSomebody gave up!")
                    sys.exit()
                int_input = True
            except ValueError:
                print("Please type in a number between 1 and 8.")
                continue
        return action


if __name__ == "__main__":
    # Crate Match Object
    match1 = Match(("player1", "player2"), start_board)
