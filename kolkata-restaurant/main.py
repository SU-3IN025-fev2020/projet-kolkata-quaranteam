from astar import *
from agent import *
from restaurant import *
# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None, fps=5):
    global player,game
    name = _boardname if _boardname is not None else 'pathfindingWorld3'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = fps  # frames per second
    game.mainiteration()
    player = game.player
    print(player)
    
def main():

    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)
    init("kolkata_6_10")
    #-------------------------------
    # Building the matrix
    #-------------------------------
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    # on localise tous les objets ramassables
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
    #-------------------------------
    # Building the best path with A*
    #-------------------------------
    # On cree le jeu
    dir_vecs = [(0,1),(1,0),(0,-1),(-1,0)]
    dims = (20,20)
    chemins = [[] for x in initStates]
    
    # Initialize agents 
    
    
    # Initialize restaurants
    restaurants = [Restaurant(x) for x in goalStates]
    
    player.set_rowcol(5,5)
    game.mainiteration()
    # Main loop
    for i in range(iterations):
        time.sleep(0.05)
        players = []
        # Spawn players at a random location
        for x in initStates:
            pass
        # Have players choose a restaurant
        pass
        # Chaque joueur se rend au restaurant de son choix en suivant le plus court chemin
        pass
        # Quand tous les joueurs soient arrivés, ils obtiennent leur gain et prennent connaissance
        # des taux de remplissage de chaque restaurant
    
    """
    j = JeuRecherche(initStates[0], goalStates[0], distManhattan, dir_vecs, dims, wallStates)
    # On applique astar
    chemin = astar(j)
        
    #-------------------------------
    # Moving along the path
    #-------------------------------
    row,col = initStates[0]
    for i in range(iterations):
        current = min(i,len(chemin)-1)
        next_row,next_col = chemin[current].etat
        player.set_rowcol(next_row,next_col)
        print("pos 1:", next_row, next_col)
        game.mainiteration()
        row,col = next_row,next_col
        if (row,col) == goalStates[0]:
            o = game.player.ramasse(game.layers)
            game.mainiteration()
            print("Objet trouvé!", o)
            break
    return
    # bon ici on fait juste un random walker pour exemple...
    

    row,col = initStates[0]
    #row2,col2 = (5,5)

    for i in range(iterations):
    
    
        x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
        next_row = row+x_inc
        next_col = col+y_inc
        if ((next_row,next_col) not in wallStates) and next_row>=0 and next_row<=20 and next_col>=0 and next_col<=20:
            player.set_rowcol(next_row,next_col)
            print ("pos 1:",next_row,next_col)
            game.mainiteration()

            col=next_col
            row=next_row

            
        
            
        # si on a  trouvé l'objet on le ramasse
        if (row,col)==goalStates[0]:
            o = game.player.ramasse(game.layers)
            game.mainiteration()
            print ("Objet trouvé!", o)
            break
        '''
        #x,y = game.player.get_pos()
    
        '''
    """
    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()
    


