from astar import *
from agent import *
from restaurant import *
from utils import *

import strategies

# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----
game = Game()
def init(_boardname=None, fps=5):
    global players,game
    name = _boardname if _boardname is not None else 'pathfindingWorld3'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = fps  # frames per second
    game.mainiteration()
    players = list(game.layers["joueur"])
    
def simulate(n, strats, iterations=100, verbose=False):
    init("kolkata_6_10",fps=30)
    p = len(players)
    stats = {}
    assert p % n == 0 and len(strats) == n
    
    initStates = [o.get_rowcol() for o in game.layers['joueur']] # Joueurs
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']] # Ramassables
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']] # Murs
    
    stats['players'] = {} # Global player statistics
    for s in strats:
        stats[s] = {} # Group statistics
    stats['restaurants'] = {} # Global restaurant statistics
    for i in range(len(goalStates)):
        stats['restaurant '+str(i+1)] = [] # Restaurant occupation statistics
    
    # On cree le jeu
    dir_vecs = [(0,1),(1,0),(0,-1),(-1,0)]
    dims = (20,20)
    
    # Initialize agents and restaurants
    restaurants = [Restaurant(x) for x in goalStates]
    n_restaurants = len(restaurants)
    occupation = [[0] for x in restaurants]
    # Spawn players at a random location
    agents = []
    for i in range(n):
        for j in range(p//n):
            agents.append(Agent(players[i*(p//n)+j],dims,dir_vecs, \
                                wallStates,occupation,getattr(strategies, strats[i])))
    n_agents = len(agents)
    
    # Main loop
    for i in range(iterations):
        # Have players choose a restaurant
        for agent in agents:
            agent.get_goal(restaurants, n=n_restaurants, occupation=occupation)
            # Chaque joueur se rend au restaurant de son choix en suivant le plus court chemin
            agent.simulate()
        # Quand les joueurs soient arrivés, ils obtiennent leur gain et prennent connaissance
        # des taux de remplissage de chaque restaurant
        for restaurant,r in zip(restaurants, range(len(restaurants))):
            occupation[r].append(len(restaurant.q)) # Record info BEFORE simulation
            restaurant.simulate()
        # More efficient memorywise to keep a global tracker of occupation
        game.mainiteration()
    
    scores = [a.score for a in agents]
    if (verbose):
        for a in agents:
            print("Player {} had a final score of {}".format(a.id, a.score))
    
    # Stat calculation
    cumulative,avg,max_score,min_score = np.sum(scores), np.average(scores), max(scores), min(scores)
    stats['players'] = {'cumulative':cumulative, 'avg':avg, 'max':max_score, 'min':min_score}
    for i,s in zip(range(n),strats):
        start = i*(p//n)
        end = i*(p//n)+(p//n)
        stats[s] = {'cumulative': np.sum(scores[start:end]), \
                    'avg': np.average(scores[start:end]), \
                    'max': max(scores[start:end]), \
                    'min': min(scores[start:end])}
    for i in range(len(restaurants)):
        stats['restaurant '+str(i+1)] = occupation[i]
    stats['restaurants']['avg'] = np.average((np.array(occupation)).flatten())
    if (verbose):
        print(r"Cumulative: {} - Average: {} - Max: {} - Min: {}".format(cumulative, avg, max_score, min_score))
    pygame.quit()
    return stats
    
def simulate_n(n=10,verbose=False):
    stats = [simulate(verbose=verbose) for _ in range(n)]
    aux = []
    for i in range(4):
        aux.append([s[i] for s in stats])
    
    global_stats = [np.average(x) for x in aux]
    if (verbose):
        print("AVGS -> Cumulative:", global_stats[0], " - Average: ", global_stats[1], " - Max: ", global_stats[2], " - Min: ", global_stats[3])
    return stats,global_stats

def main():
    iterations=100
    repeat=1
    if len(sys.argv) >= 2:
        iterations = int(sys.argv[1])
    if len(sys.argv) == 3:
        repeat = int(sys.argv[2])
    assert repeat > 0
    
    for _ in range(repeat):
        simulate(2,['random_obstinate','uniformly_random'],verbose=True)
   

if __name__ == '__main__':
    main()
    


