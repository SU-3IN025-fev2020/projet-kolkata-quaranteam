# Strategies
import numpy as np

def random_obstinate(n, previous):
    return previous if (previous != -1) else random.randint(0,n-1)
    
def uniformly_random(n):
    return random.randint(0,n-1)

def min_occupation_forgetful(n, occupation):
    choice = 0
    for i in range(1,n):
        if(occupation[-1,i] < occupation[-1,i]):
            choice = i
    return choice

def min_occupation_min_distance_forgetful(n, occupation, distances, w_occupation=0.5, w_distance=0.5):
    choice = 0
    score = occupation[0]*w_occupation+distances[0]*w_distance
    for i in range(1,n):
        if(occupation[i]*w_occupation+distances[i]*w_distance < score):
            choice = i
            score = occupation[i]*w_occupation+distances[i]*w_distance
    return choice

def min_occupation_avg(n,occupation):
    avgs = []
    choice = 0
    for i in range(1,n):
        if(avgs[i] < avgs[choice]):
            choice = i
    return choice