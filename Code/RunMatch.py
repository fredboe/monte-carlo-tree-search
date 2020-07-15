# from collections import namedtuple
import sys
from Game.GameStateConnect4 import GameState

"""Games = namedtuple("Games", "Connect4")
games = Games(GameState)"""

start_board_list = ["0" for i in range(0, 56)]
start_board = "".join(start_board_list)


class Match:

    def __init__(self, agents, start_board):
        self.agent_player, self.agent_opponent = agents
        self.start_board = start_board
        self.initialGameState = GameState(start_board, 1)
        self.run_Match(self.initialGameState)

    def get_action_from_agent(self):
        pass

    def run_Match(self, GameState):
        while not GameState.terminal_state():
            action = self.get_action_from_realWorld()
            if action not in GameState.actions:
                print("\n\nSorry, but this action isn't AVAILABLE.\n\n")
                continue
            GameState = GameState.result(action)
            print(str(GameState))
        winner = GameState.winner()
        print("Player "+str(winner)+" has won." if winner else "Nobody won!")

    def get_action_from_realWorld(self):
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
            except Exception:
                continue
        return action


if __name__ == "__main__":
    """str_game = "Connect4"
    agent_player = ""
    agent_opponent = ""
    game = games[str_game]"""
    # Crate Match Object
    match1 = Match(("player1", "player2"), start_board)
