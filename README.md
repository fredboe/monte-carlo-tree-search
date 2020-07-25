# monte-carlo-tree-search

## Project
This project contains a basic implementation of the Monte Carlo Tree Search.
Furthermore, you can find some other agents (AlphaBeta, Random) which you can try out against MCTS.

For those who find this algorithm interesting I will also add some further reading/information below.

## Code
I would be really pleased about some suggested improvements for my code or other stuff like documentation.

## Execute the code
### The first execution
To see a first result just execute RunMatch.py
```
python RunMatch.py
```
### Changing the agents
To change the agents you just need to change the first parameter in the Match obj. The possible agents are "MCTS", "REALWORLD" (you can play), "ALPHABETA", "RANDOM".
```
match = Match(("MCTS", "ALPHABETA"), start_board)
```
### Change some parameters
There are some parameters you can change to experiment with the results.    
For example, you can change the depth in AlphaBeta.py (line 6)
```
def get_action(self, state, player_id, depth=6):
```
another parameter you can change is max_time in MCTS.py (line 129). With this you can change the duration of MCTS.
```
def runMCTS(self, player_id, max_time=5):
```

## Further readings
* https://www.aaai.org/Papers/AIIDE/2008/AIIDE08-036.pdf
* https://www.youtube.com/watch?v=UXW2yZndl7U
* http://www.diego-perez.net/papers/MCTSSurvey.pdf
* https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
