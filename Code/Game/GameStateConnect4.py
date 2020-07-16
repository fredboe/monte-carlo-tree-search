import re

STR_DIAG1 = "(1.......1.......1.......1)|(2.......2.......2.......2)"
STR_DIAG2 = "(1.....1.....1.....1)|(2.....2.....2.....2)"
STR_ROWS = "(1......1......1......1)|(2......2......2......2)"
STR_COLS = "(1111)|(2222)"


class GameState:

    def __init__(self, board, player_id):
        self.board = board
        self.board2 = re.sub(" ", "", self.board)
        self.player_id = player_id
        self.win_player1 = [1, 1, 1, 1]
        self.win_player2 = [2, 2, 2, 2]
        self.actions = self.possible_actions()
        self.winner = self.winner()
        # self.cols = deepcopy(board)
        # self.rows = list(zip(*board))

    def __str__(self):
        headline = "Connect 4".center(23, "-")
        length = len(self.board2)
        print(length)
        cols = [self.board2[cell:cell+6][::-1] for cell in range(0, length, 6)]
        rows = list(zip(*cols))
        str_board = ""
        for row in rows:
            str_board += "  ".join(row)
            str_board += "\n"
        end = ""
        if self.winner:
            #print(self.terminal_state())
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
        #print(col_index+i_of_zero)
        board = self.create_new_board(board, col_index+i_of_zero)
        new_player_id = self.new_player_id()
        return GameState(board, new_player_id)

    def create_new_board(self, board, in_str):
        return board[:in_str]+str(self.player_id)+board[in_str+1:]

    def new_player_id(self):
        return self.player_id % 2 + 1

    def terminal_state(self):
        return True if self.winner or not self.has_actions() else False

    # winner as getter and setter
    def winner(self):
        win = re.search(STR_COLS+"|"+STR_ROWS+"|"+STR_DIAG1+"|"+STR_DIAG2, self.board)
        if win:
            return int(win.group()[0])
        return 0

    def utility2(self, player):
        if not self.winner:
            return 0
        return 5 if self.winner == player else -2
