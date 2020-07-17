import re

STR_DIAG1 = "(1.......1.......1.......1)|(2.......2.......2.......2)"
STR_DIAG2 = "(1.....1.....1.....1)|(1.....1.....1.....1)"
STR_ROWS = "(1......1......1......1)|(2......2......2......2)"
STR_COLS = "(1111)|(2222)"


class GameState:

    def __init__(self, board, player_id):
        self.board = board
        self.player_id = player_id
        self.win_player1 = [1, 1, 1, 1]
        self.win_player2 = [2, 2, 2, 2]
        # self.cols = deepcopy(board)
        # self.rows = list(zip(*board))

    def __str__(self):
        headline = "Connect 4".center(21, "#")
        cols = [self.board[cell:cell+7] for cell in range(0, len(self.board), 7)]
        rows = list(zip(*cols))
        str_board = ""
        for row in rows:
            str_board += "  ".join(row)
            str_board += "\n"
        end = ""
        winner = self.winner()
        if winner:
            end += "The winner is Player "+str(winner)
        return headline+"\n\n"+str_board+"\n"+end

    @property
    def player_id(self):
        return self.player_id

    def possible_actions(self):
        important_cells = self.board[6:][::7].copy()
        return [index for index in range(0, len(important_cells)) if important_cells[index] == '0']
        # return [self.board.index(col) for col in self.board if col[-1]==0]

    """def has_actions(self):
        return any(self.possible_actions(self.board))"""

    def result(self, action):
        if self.terminal_state():
            return None
        board = self.board.copy()
        action_col_list_index = action*7
        index_of_zero = board[action_col_list_index:].index('0')
        board[action_col_list_index+index_of_zero] = self.player_id
        new_player_id = self.new_player_id()
        return GameState(board, new_player_id)

    def new_player_id(self):
        return self.player_id % 2 + 1

    def terminal_state(self):
        return True if self.winner() else False

    def winner(self):
        win = re.search(STR_COLS+"|"+STR_ROWS+"|"+STR_DIAG1+"|"+STR_DIAG2, self.board)
        if win:
            return win.group()[0]
        return 0

    def utility(self):
        winner = self.winner()
        if not winner:
            return None
        return 1 if winner == self.player_id else 0
