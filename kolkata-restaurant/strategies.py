# Strategies (we want a uniform function signature)
import numpy as np
from utils import *

def random_obstinate(pos, last, n, restaurants, occupation):
    return last if (last != -1) else random.randint(0,n-1)
    
def uniformly_random(pos, last, n, restaurants, occupation):
    return random.randint(0,n-1)

def min_distance(pos, last, n, restaurants, occupation):
    dists = [distManhattan(pos,r.pos) for r in restaurants]
    choice = 0
    for i in range(1,len(dists)):
        if(dists[i] < dists[choice]):
            choice = i
    return choice

def min_occupation_forgetful(pos, last, n, restaurants, occupation):
    choice = 0
    for i in range(1,n):
        if(occupation[i][-1] < occupation[choice][-1]):
            choice = i
    return choice

def min_occupation_avg(pos, last, n, restaurants, occupation):
    avgs = [np.average(o) for o in occupation] #TO DO: Calculate averages
    choice = 0
    for i in range(1,n):
        if(avgs[i] < avgs[choice]):
            choice = i
    return choice