import re

# strings for the possible winning positions (for RegEx)
STR_DIAG1 = "(1.......1.......1.......1)|(2.......2.......2.......2)"
STR_DIAG2 = "(1.....1.....1.....1)|(2.....2.....2.....2)"
STR_ROWS = "(1......1......1......1)|(2......2......2......2)"
STR_COLS = "(1111)|(2222)"

# strings for all diags, rows, cols that a player can still win with
STR_EVAL = "(0|2.......0|2.......0|2.......0|2)|(0|2.....0|2.....0|2.....0|2)|(0|2......0|2......0|2......0|2)|(0|20|20|20|2)"
STR_EVAL_OPP = "(0|1.......0|1.......0|1.......0|1)|(0|1.....0|1.....0|1.....0|1)|(0|1......0|1......0|1......0|1)|(0|10|10|10|1)"


class GameState:

    def __init__(self, board, player_id):
        # board string
        self.board = board
        # board string without whitespaces
        self.board2 = re.sub(" ", "", self.board)
        # player_id: int
        self.player_id = player_id
        # possible actions: list
        self.actions = self.possible_actions()
        # winner of the GameState: player_id if there is a winner else 0
        self.winner = self.winner()

    def __str__(self):
        """
            returns the board as a string so that it can be printed
        """
        headline = "Connect 4".center(19, "-")
        length = len(self.board2)
        cols = [self.board2[cell:cell+6][::-1] for cell in range(0, length, 6)]
        rows = list(zip(*cols))
        str_board = ""
        for row in rows:
            str_board += "  ".join(row)
            str_board += "\n"
        end = ""
        if self.winner:
            end += "The winner is Player "+str(self.winner)
        return headline+"\n\n"+str_board+"\n"+end

    @property
    def get_actions(self):
        """
            returns the possible actions of the GameState
        """
        return self.actions

    @get_actions.setter
    def set_actions(self, actions):
        """
            sets the actions
        """
        self.actions = actions

    @property
    def get_player_id(self):
        """
            return the player_id 1 or 2
        """
        return self.player_id

    @get_player_id.setter
    def set_player_id(self, player_id):
        """
            sets the player_id: int
        """
        self.player_id = player_id

    @property
    def get_winner(self):
        """
            return winner player_id (1 or 2) or 0 if there is no winner
        """
        return self.winner

    @get_winner.setter
    def set_winner(self, winner):
        """
            sets the winner: int
        """
        self.winner = winner

    def possible_actions(self):
        """
            returns all possible actions (list of int) of the GameState
        """
        important_cells = self.board2[5:][::6]
        length = len(important_cells)
        return [i+1 for i in range(0, length) if important_cells[i] == '0']

    def has_actions(self):
        """
            returns True if self.actions is not empty else False
        """
        return any(self.actions)

    def result(self, action):
        """
            parameters:
                        action: int
            returns:
                    new GameState (result of the action)
        """
        if self.terminal_state():
            return None
        board = self.board
        col_index = (action-1)*7
        i_of_zero = board[col_index:col_index+7].index('0')
        board = self.create_new_board(board, col_index+i_of_zero)
        new_player_id = self.new_player_id()
        return GameState(board, new_player_id)

    def create_new_board(self, board, in_str):
        """
            parameters:
                        board: string
                        in_string: int (index of the board string)
            returns:
                    new board string after changing the string at in_string
        """
        return board[:in_str]+str(self.player_id)+board[in_str+1:]

    def new_player_id(self):
        """
            returns:
                    new player_id (int 1 or 2) ->toggles between 1 and 2
        """
        return self.player_id % 2 + 1

    def terminal_state(self):
        """
            returns:
                    True if there is a winner or the board if full else False
        """
        return True if self.winner or not self.has_actions() else False

    def winner(self):
        """
            returns:
            the winner of the game: int player_id if there is a winner else 0
        """
        win = re.search(STR_COLS+"|"+STR_ROWS+"|"+STR_DIAG1+"|"+STR_DIAG2, self.board)
        if win:
            return int(win.group()[0])
        return 0

    def utility(self, player):
        """
            returns:
                    utility (+inf or -inf) for ALPHABETA
        """
        if not self.winner:
            return 0
        return float("inf") if self.winner == player else float("-inf")

    def utility2(self, player):
        """
            returns:
                    utility (1 or -1) for MCTS

        """
        if not self.winner:
            return 0
        return 1 if self.winner == player else -1

    def count_evaluation(self):
        """
        returns:
                possible winning positions of player
                minus possible winning positions of the opponent
        """
        possible_win_comb = len(re.findall(STR_EVAL, self.board))
        possible_win_comb_opp = len(re.findall(STR_EVAL_OPP, self.board))
        return possible_win_comb-possible_win_comb_opp
