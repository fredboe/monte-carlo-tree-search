from copy import deepcopy

class GameState:

    def __init__(self, board, player_id):
        self.board = board
        self.player_id = player_id
        self.cols = deepcopy(board)
        self.rows = list(zip(*board))
        #diags1=
        #diags2=


    @property
    def player_id(self):
        return self.player_id

    def possible_actions(self):
        return [self.board.index(col) for col in self.board if col[-1]==0]#TODO

    def has_actions(self):
        return any(self.possible_actions(self.board))

    def result(self, action):
        board = deepcopy(self.board)
        board[action].insert(self.player_id, board[action].index(0))
        new_player_id = self.new_player_id()
        return GameState(board, new_player_id)

    def new_player_id(self):
        return self.player_id % 2 + 1

    def is_winner(self):
        pass

    def utility(self):
        winner = self.is_winner()
        if not winner:
            return None
        return 1 if winner == self.player_id else 0