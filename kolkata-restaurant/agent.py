from astar import *
import random

class Agent:

    def __init__(self, player, pos, dims, dir_vecs, walls, strategy):
        self.player = player
        self.pos = pos
        self.dims = dims
        self.dir_vecs = dir_vecs
        self.walls = walls
        self.strategy = strategy
        self.score = 0
    
    def get_goal(self, restaurants, *args, **kwargs):
        goal_idx = self.strategy(args, kwargs)
        self.goal = restaurants[goal_idx]
    
    def find_path(self):
        j = JeuRecherche(self.pos, self.goal.pos, distManhattan, self.dir_vecs, self.dims, self.walls)
        self.path = astar(j)
        self.current = 0
    
    """Simulate a step towards the current goal."""
    def simulate(self):
        if(self.current < len(self.path)-1):
            self.current += 1
            self.pos = self.path[self.current]
            next_row, next_col = self.pos
            self.player.set_rowcol(next_row, next_col)
        
        
# Define some strategies

def random_obstinate(n, previous):
    return previous if (previous != -1) else random.randint(0,n-1)
    
def uniformly_random(n):
    return random.randint(0,n-1)

def min_occupation(n, occupation):
    pass

def min_occupation_min_distance(n, occupation, restaurants):
    pass