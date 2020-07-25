import sys
# import the GameState of the game
from Game.GameStateConnect4 import GameState
# import all agents
from Agents.MCTS import MCTSTree
from Agents.Random import RandomAgent
from Agents.AlphaBeta import AlphaBetaAgent

# creates the board string for connect4 (full of zeros)
start_board_list = ["000000 " for i in range(0, 7)]
start_board = "".join(start_board_list)


class Match:

    def __init__(self, agents, start_board):
        # names of agents: string
        self.agent1, self.agent2 = agents
        # board: string
        self.start_board = start_board
        # initial GameState: GameState
        self.initialState = GameState(start_board, 1)
        # functions of the agents: returns action (int)
        self.func_agent1 = getattr(self, self.agent1)
        self.func_agent2 = getattr(self, self.agent2)
        # runs the match
        self.run_Match(self.initialState)

    def MCTS(self, state):
        """
            returns:
                    the result of MCTS agent (action int)
        """
        player_id = state.player_id
        return MCTSTree(state).runMCTS(player_id)

    def RANDOM(self, state):
        """
            returns:
                    the result of RANDOM agent (action int)
        """
        return RandomAgent().get_action(state)

    def ALPHABETA(self, state):
        """
            returns:
                    the result of ALPHABETA agent (action int)
        """
        player_id = state.player_id
        return AlphaBetaAgent().get_action(state, player_id)

    def REALWORLD(self, state):
        """
            returns:
                    action -> you can choose the action
                    -type in a number between 1 and 8
        """
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
        """
            runs the match: asks for actions until the game is over
                            then prints the winner
        """
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
    """ Create Match Object
        first parameter = agents (choose between "MCTS", "ALPHABETA",
                                                 "RANDOM", "REALWORLD")
        second parameter = start_board (string)
        """
    match = Match(("MCTS", "ALPHABETA"), start_board)
