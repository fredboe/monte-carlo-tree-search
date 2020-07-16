class AlphaBetaAgent:

    def get_action(self, state, depth=4):
        for action in state.actions:
            new_state=state.result(action)
            if new_state.terminal_state() and new_state.winner:
                print("TEst")
                return action
        return self.alpha_beta_search(state, depth)

    def alpha_beta_search(self, state, depth):
        alpha = float("-inf")
        beta = float("inf")

        def min_value(state, alpha, beta, depth):
            if state.terminal_state():
                return state.utility(2)
            if depth <= 0:
                return self.evaluation_function(state)
            value = float("inf")
            for action in state.actions:
                value = min(value, max_value(state.result(action), alpha, beta, depth-1))
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value

        def max_value(state, alpha, beta, depth):
            if state.terminal_state():
                return state.utility(2)
            if depth <= 0:
                return self.evaluation_function(state)
            value = float("-inf")
            for action in state.actions:
                value = max(value, min_value(state.result(action), alpha, beta, depth-1))
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value
        print("TEST")
        print(max(state.actions, key=lambda x: min_value(state.result(x), alpha, beta, depth-1)))
        return max(state.actions, key=lambda x: min_value(state.result(x), alpha, beta, depth-1))

    def evaluation_function(self, state):
        #print(state.count_evaluation())
        return state.count_evaluation()
