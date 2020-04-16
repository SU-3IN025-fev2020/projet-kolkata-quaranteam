from collections import deque

def Restaurant:

    def __init__(self, pos):
        self.pos = pos
        self.q = deque()
        
    def new_customer(self, customer):
        self.q.append(customer)
        
    def simulate(self):
        # Serves the next customer waiting
        x = self.q.popleft()
        x.score += 1