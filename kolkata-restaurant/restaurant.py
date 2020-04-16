from collections import deque

class Restaurant:
    idgen = 1
    
    def __init__(self, pos):
        self.id = Restaurant.idgen
        Restaurant.idgen += 1
        
        self.pos = pos
        self.q = deque()
        
    def new_customer(self, customer):
        self.q.append(customer)
        
    def simulate(self):
        # Serves the next customer waiting
        if self.q:
            x = self.q.popleft()
            #print("Restaurant {} processed agent {}".format(self.id, x.id))
            x.score += 1
            x.moving = False # Allows agent to move again
            x.waiting = False