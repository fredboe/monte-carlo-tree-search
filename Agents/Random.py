import random


class RandomAgent:

    def get_action(self, state):
        """
            parameters:
                        state: GameState
            returns
                    random action of the possible actions
        """
        return random.choice(state.actions)
