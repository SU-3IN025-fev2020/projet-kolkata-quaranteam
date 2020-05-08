from collections import deque

class Restaurant:
    """Class representing a restaurant."""
    idgen = 1
    
    def __init__(self, pos, verbose=False):
        """Initialize the restaurant."""
        self.id = Restaurant.idgen
        Restaurant.idgen += 1
        
        self.pos = pos
        self.q = deque()
        self.verbose = verbose
        
    def new_customer(self, customer):
        """Adds a new customer to the queue."""
        self.q.append(customer)
        
    def simulate(self):
        """Advances a step in the simulation."""
        # Serves the next customer waiting
        if self.q:
            x = self.q.popleft()
            if(self.verbose):
                print("Restaurant {} processed agent {}".format(self.id, x.id))
            x.score += 1
            x.moving = False # Allows agent to move again
            x.waiting = False