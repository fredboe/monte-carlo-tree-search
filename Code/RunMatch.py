from collections import namedtuple

from Game import GameStateConnect4

Games = namedtuple("Games", "Connect4")
games = Games(GameStateConnect4)


class Match:
    pass


if __name__ == "__main__":
    str_game = "Connect4"
    agent_player = ""
    agent_opponent = ""
    game = games[str_game]
    # Crate Match Object
