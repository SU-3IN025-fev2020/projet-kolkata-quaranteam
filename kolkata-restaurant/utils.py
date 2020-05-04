import random

def random_position(dims, walls):
    r,c = dims
    pos = (random.randint(0,r-1), random.randint(0,c-1))
    while(pos in walls):
        pos = (random.randint(0,r-1), random.randint(0,c-1))
    return pos
    
def distManhattan(p1,p2):
    """ calcule la distance de Manhattan entre le tuple 
        p1 et le tuple p2
        """
    (x1,y1)=p1
    (x2,y2)=p2
    return abs(x1-x2)+abs(y1-y2)