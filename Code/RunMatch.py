from Game import GameStateConnect4

gameDic = {"Connect 4": GameStateConnect4}


class Match:
    pass


if __name__ == "__main__":
    str_game = "Connect 4"
    agent_player = ""
    agent_opponent = ""
    # Crate Match Object


def getGame(str_game):
    return gameDic[str_game]
