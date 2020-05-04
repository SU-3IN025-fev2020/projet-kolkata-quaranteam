from astar import *
from utils import *
import random

class Agent:
    """Class representing an agent."""
    idgen = 1

    def __init__(self, player, dims, dir_vecs, walls, occupation, strategy, verbose=False):
        """Initialize the agent."""
        self.id = Agent.idgen
        Agent.idgen += 1
        self.player = player
        self.pos = random_position(dims, walls)
        self.dims = dims
        self.dir_vecs = dir_vecs
        self.walls = walls
        self.occupation = occupation
        self.strategy = strategy
        self.score = 0
        self.current = 0
        self.moving = False
        self.waiting = False
        self.goal_idx = -1
        self.verbose = verbose
    
    def get_goal(self, restaurants, *args, **kwargs):
        """Get goal from current strategy."""
        if not self.moving:
            self.goal_idx = self.strategy(*args, **kwargs)
            self.goal = restaurants[self.goal_idx]
            self.find_path()
            self.moving = True
    
    def find_path(self):
        """Find path towards current goal."""
        j = JeuRecherche(self.pos, self.goal.pos, distManhattan, self.dir_vecs, self.dims, self.walls)
        self.path = astar(j)
        self.current = 0
        if(self.verbose):
            print("Player {} moving towards Restaurant {}.".format(self.id, self.goal.id))
    
    def simulate(self):
        """Simulate a step towards the current goal."""
        if(self.current < len(self.path)-1):
            self.current += 1
            self.pos = self.path[self.current].etat #Object of type Node!
            next_row, next_col = self.pos
            self.player.set_rowcol(next_row, next_col)
        if(self.current >= len(self.path)-1 and not self.waiting):
            self.goal.new_customer(self)
            self.waiting = True
        
        
# Define some strategies

def random_obstinate(n, previous):
    return previous if (previous != -1) else random.randint(0,n-1)
    
def uniformly_random(n):
    return random.randint(0,n-1)

def min_occupation(n, occupation):
    pass

def min_occupation_min_distance(n, occupation, restaurants):
    pass