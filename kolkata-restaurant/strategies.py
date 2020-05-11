# Strategies (we want a uniform function signature)
import numpy as np
import random

from utils import *

def random_obstinate(pos, last, n, restaurants, occupation):
    return last if (last != -1) else random.randint(0,n-1)
    
def uniformly_random(pos, last, n, restaurants, occupation):
    return random.randint(0,n-1)

# Strategies with pooling (to avoid clumps of agents)

def min_distance(pos, last, n, restaurants, occupation):
    dists = [distManhattan(pos,r.pos) for r in restaurants]
    pool = [0]
    for i in range(1,len(dists)):
        if(dists[i] < dists[pool[0]]):
            pool = [i]
        elif (dists[i] == dists[pool[0]]):
            pool.append(i)
    return random.choice(pool)

def min_occupation_forgetful(pos, last, n, restaurants, occupation):
    pool = [0]
    for i in range(1,n):
        if(occupation[i][-1] < occupation[pool[0]][-1]):
            pool = [i]
        elif(occupation[i][-1] == occupation[pool[0]][-1]):
            pool.append(i)
    return random.choice(pool)

def min_occupation_avg(pos, last, n, restaurants, occupation):
    avgs = [np.average(o) for o in occupation]
    pool = [0]
    for i in range(1,n):
        if(avgs[i] < avgs[pool[0]]):
            pool = [i]
        elif(avgs[i] == avgs[pool[0]]):
            pool.append(i)
    return random.choice(pool)
    
def stochastic(pos, last, n, restaurants, occupation):
    z = np.sum([np.exp(-occupation[k][-1]) for k in range(n)])
    probs = [(np.exp(-occupation[k][-1]))/z for k in range(n)]
    return np.random.choice(range(n),p=probs)