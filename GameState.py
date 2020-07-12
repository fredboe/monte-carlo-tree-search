from copy import deepcopy
#import re

class GameState:

    def __init__(self, board, player_id,rows,cols,diags):
        self.board = board
        self.player_id = player_id
        self.poss_wins=rows+cols+diags
        self.win_player1=[1,1,1,1]
        self.win_player2=[2,2,2,2]
        #self.cols = deepcopy(board)
        #self.rows = list(zip(*board))
        

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
        if self.win_player1 in self.poss_wins:
            return 1
        elif self.win_player2 in self.poss_wins:
            return 2
        else:
            return 0

    def utility(self):
        winner = self.is_winner()
        if not winner:
            return None
        return 1 if winner == self.player_id else 0