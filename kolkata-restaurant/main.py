from astar import *
from agent import *
from restaurant import *
from utils import *

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
    
def main(repeat=10):
    assert repeat > 0
    stats = []
    for _ in range(repeat):
        
        #for arg in sys.argv:
        iterations = 100 # default
        if len(sys.argv) == 2:
            iterations = int(sys.argv[1])
        print ("Iterations: ")
        print (iterations)
        init("kolkata_6_10",fps=30)
        #-------------------------------
        # Building the matrix
        #-------------------------------
        # on localise tous les états initiaux (loc du joueur)
        initStates = [o.get_rowcol() for o in game.layers['joueur']]
        # on localise tous les objets ramassables
        goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
        # on localise tous les murs
        wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
        # On cree le jeu
        dir_vecs = [(0,1),(1,0),(0,-1),(-1,0)]
        dims = (20,20)
        chemins = [[] for x in initStates]
        # Initialize agents and restaurants
        restaurants = [Restaurant(x) for x in goalStates]
        n_restaurants = len(restaurants)
        occupation = [[0] for x in restaurants]
        # Spawn players at a random location
        agents = [Agent(p,dims,dir_vecs,wallStates,occupation,min_occupation_avg) for p in players]
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
                restaurant.simulate()
                occupation[r].append(len(restaurant.q))
            # More efficient memorywise to keep a global tracker of occupation
            game.mainiteration()
        
        scores = [a.score for a in agents]
        for a in agents:
            print("Player {} had a final score of {}".format(a.id, a.score))
        
        cumulative,avg,max_score,min_score = np.sum(scores), np.average(scores), max(scores), min(scores)
        aux = [cumulative,avg,max_score,min_score]
        print(r"Cumulative: {} - Average: {} - Max: {} - Min: {}".format(cumulative, avg, max_score, min_score))
        pygame.quit()
        stats.append(aux)
    for s,i in zip(stats,range(len(stats))):
        print(r'Stats for repetition {}: {}'.format(i+1,s))
    
    a1,a2,a3 = [s[0] for s in stats], [s[1] for s in stats],[s[2] for s in stats]
    a4 = [s[3] for s in stats]
    print("AVGS -> Cumulative:", np.average(a1), " - Average: ", np.average(a2), " - Max: ", np.average(a3), " - Min: ", np.average(a4))
    
   

if __name__ == '__main__':
    main()
    


