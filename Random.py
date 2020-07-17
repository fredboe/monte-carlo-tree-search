import random


class RandomAgent:

    def get_action(self, state):
        return random.choice(state.actions)
