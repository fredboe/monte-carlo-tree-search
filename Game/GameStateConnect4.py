import re

STR_DIAG1 = "(1.......1.......1.......1)|(2.......2.......2.......2)"
STR_DIAG2 = "(1.....1.....1.....1)|(2.....2.....2.....2)"
STR_ROWS = "(1......1......1......1)|(2......2......2......2)"
STR_COLS = "(1111)|(2222)"

STR_EVAL = "(0|2.......0|2.......0|2.......0|2)|(0|2.....0|2.....0|2.....0|2)|(0|2......0|2......0|2......0|2)|(0|20|20|20|2)"
STR_EVAL_OPP = "(0|1.......0|1.......0|1.......0|1)|(0|1.....0|1.....0|1.....0|1)|(0|1......0|1......0|1......0|1)|(0|10|10|10|1)"


class GameState:

    def __init__(self, board, player_id):
        self.board = board
        self.board2 = re.sub(" ", "", self.board)
        self.player_id = player_id
        self.actions = self.possible_actions()
        self.winner = self.winner()

    def __str__(self):
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
        return self.actions

    @get_actions.setter
    def set_actions(self, actions):
        self.actions = actions

    @property
    def get_player_id(self):
        return self.player_id

    @get_player_id.setter
    def set_player_id(self, player_id):
        self.player_id = player_id

    @property
    def get_winner(self):
        return self.winner

    @get_winner.setter
    def set_winner(self, winner):
        self.winner = winner

    def possible_actions(self):
        important_cells = self.board2[5:][::6]
        length = len(important_cells)
        return [i+1 for i in range(0, length) if important_cells[i] == '0']

    def has_actions(self):
        return any(self.actions)

    def result(self, action):
        if self.terminal_state():
            return None
        board = self.board
        col_index = (action-1)*7
        i_of_zero = board[col_index:col_index+7].index('0')
        board = self.create_new_board(board, col_index+i_of_zero)
        new_player_id = self.new_player_id()
        return GameState(board, new_player_id)

    def create_new_board(self, board, in_str):
        return board[:in_str]+str(self.player_id)+board[in_str+1:]

    def new_player_id(self):
        return self.player_id % 2 + 1

    def terminal_state(self):
        return True if self.winner or not self.has_actions() else False

    def winner(self):
        win = re.search(STR_COLS+"|"+STR_ROWS+"|"+STR_DIAG1+"|"+STR_DIAG2, self.board)
        if win:
            return int(win.group()[0])
        return 0

    def utility(self, player):
        if not self.winner:
            return 0
        return float("inf") if self.winner == player else float("-inf")

    def utility2(self, player):
        if not self.winner:
            return 0
        return 1 if self.winner == player else -1

    def count_evaluation(self):
        possible_win_comb = len(re.findall(STR_EVAL, self.board))
        possible_win_comb_opp = len(re.findall(STR_EVAL_OPP, self.board))
        return possible_win_comb-possible_win_comb_opp