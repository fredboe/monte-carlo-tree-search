class AlphaBetaAgent:

    def get_action(self, state, depth=5):
        """
        
        Parameters:
                    state: obj GameState
                    depth: int
        returns
                action: int (result of alpha_beta_search)
        
        """
        return self.alpha_beta_search(state, depth)

    def alpha_beta_search(self, state, depth):
        """
        
        Parameters:
                    state: obj GameState
                    depth: int
        returns
                action: int
        
        """
        alpha = float("-inf")
        beta = float("inf")

        def min_value(state, alpha, beta, depth):
            """
            
            Parameters:
                        state
                        alpha: float (best score for max)
                        beta: float (best score for min)
                        depth: int (depth of the algorithm the tree search should go)
            returns
                    min value of the child nodes
            
            """
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
            """
            
            Parameters:
                        state
                        alpha: float (best score for max)
                        beta: float (best score for min)
                        depth: int (depth of the algorithm the tree search should go)
            returns
                    max value of the child nodes
                    
            """
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
        return max(state.actions, key=lambda x: min_value(state.result(x), alpha, beta, depth-1))

    def evaluation_function(self, state):
        """
        
        Parameters:
                    state: obj GameState
        returns
                number of still possible win situation
                minus number of possible win situations of the opponent
        
        """
        return state.count_evaluation()
