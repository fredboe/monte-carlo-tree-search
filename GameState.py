from copy import deepcopy
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

    @property
    def player_id(self):
        return self.player_id

    def possible_actions(self):
        important_cells = deepcopy(self.board[6:][::7])
        return [index for index in range(0, len(important_cells)) if important_cells[index] == '0']
        # return [self.board.index(col) for col in self.board if col[-1]==0]

    def has_actions(self):
        return any(self.possible_actions(self.board))

    def result(self, action):
        board = deepcopy(self.board)
        action_col_list_index = action*7
        index_of_zero = board[action_col_list_index:].index('0')
        board[action*7+index_of_zero] = self.player_id
        new_player_id = self.new_player_id()
        return GameState(board, new_player_id)

    def new_player_id(self):
        return self.player_id % 2 + 1

    def is_winner(self):
        # here with re
        pass

    def utility(self):
        winner = self.is_winner()
        if not winner:
            return None
        return 1 if winner == self.player_id else 0
