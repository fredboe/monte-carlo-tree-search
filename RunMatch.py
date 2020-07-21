import sys
from Game.GameStateConnect4 import GameState
from Agents.MCTS import MCTSTree
from Agents.Random import RandomAgent
from Agents.AlphaBeta import AlphaBetaAgent


start_board_list = ["000000 " for i in range(0, 7)]
start_board = "".join(start_board_list)


class Match:

    def __init__(self, agents, start_board):
        self.agent1, self.agent2 = agents
        self.start_board = start_board
        self.initialState = GameState(start_board, 1)
        self.func_agent1 = getattr(self, self.agent1)
        self.func_agent2 = getattr(self, self.agent2)
        self.run_Match(self.initialState)

    def MCTS(self, state):
        player_id = state.player_id
        return MCTSTree(state).runMCTS(player_id)

    def RANDOM(self, state):
        return RandomAgent().get_action(state)

    def ALPHABETA(self, state):
        player_id = state.player_id
        return AlphaBetaAgent().get_action(state, player_id)

    def REALWORLD(self, state):
        int_input = False
        action = None
        while not int_input:
            try:
                action = int(input("Please type in your action. "
                                   + "It has to be a number between 1 and 7."
                                   + "Type in 0 to stop the game!"))
                if action == 0:
                    print("\nSomebody gave up!")
                    sys.exit()
                int_input = True
            except ValueError:
                print("Please type in a number between 1 and 7.")
                continue
            return action

    def run_Match(self, state):
        while not state.terminal_state():
            if state.player_id == 1:
                action = self.func_agent1(state)
                print(self.agent1 + " plays action: "+str(action))
            else:
                action = self.func_agent2(state)
                print(self.agent2 + " plays action: "+str(action))
            if action not in state.actions:
                print("\n\nSorry, but this action isn't AVAILABLE.\n\n")
                continue
            state = state.result(action)
            print(str(state))
        winner = state.winner
        print("Player "+str(winner)+" has won." if winner else "Nobody won!")


if __name__ == "__main__":
    # Crate Match Object
    match1 = Match(("MCTS", "ALPHABETA"), start_board)
