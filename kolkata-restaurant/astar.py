# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
from abc import ABCMeta,abstractmethod
import pygame
import glo

import functools
import random 
import numpy as np
import sys
import heapq
import time

# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----
def distManhattan(p1,p2):
    """ calcule la distance de Manhattan entre le tuple 
        p1 et le tuple p2
        """
    (x1,y1)=p1
    (x2,y2)=p2
    return abs(x1-x2)+abs(y1-y2)

class Probleme(object):
    """ On definit un probleme comme étant: 
        - un état initial
        - un état but
        - une heuristique
        """
        
    def __init__(self,init,but,heuristique):
        self.init=init
        self.but=but
        self.heuristique=heuristique
        
    @abstractmethod
    def estBut(self,e):
        """ retourne vrai si l'état e est un état but
            """
        pass
        
    @abstractmethod
    def cost(self,e1,e2):
        """ donne le cout d'une action entre e1 et e2, 
            """
        pass
        
    @abstractmethod
    def successeurs(self,etat):
        """ retourne une liste avec les successeurs possibles
            """
        pass
        
    @abstractmethod
    def immatriculation(self,etat):
        """ génère une chaine permettant d'identifier un état de manière unique
            """
        pass

class JeuRecherche(Probleme):
    def __init__(self, init, but, heuristique, dirvecs, board_size, walls):
        super().__init__(init,but,heuristique)
        self.dirvecs = [np.array(dir) for dir in dirvecs]
        self.board_size = board_size
        self.walls = set(walls)

    def estBut(self, e):
        return e == self.but
    
    def cost(self,e1,e2):
        return distManhattan(e1,e2)
    
    def valid(self, etat):
        (mx, my) = self.board_size
        (x,y) = list(etat)
        return  (x >= 0 and y >= 0 and x < mx and y < my and (x,y) not in self.walls)

    def successeurs(self,etat):
        candidates = [np.array(etat) + dir for dir in self.dirvecs]
        return [tuple(c) for c in candidates if (self.valid(etat))]
    
    def immatriculation(self, etat):
        return "(" + str(etat[0]) + "," + str(etat[1]) + ")"
    
    def h_value(self, e1, e2):
       return distManhattan(e1, e2)

@functools.total_ordering # to provide comparison of nodes
class Noeud:
    def __init__(self, etat, g, pere=None):
        self.etat = etat
        self.g = g
        self.pere = pere
        
    def __str__(self):
        #return np.array_str(self.etat) + "valeur=" + str(self.g)
        return str(self.etat) + "valeur=" + str(self.g)
        
    def __eq__(self, other):
        return str(self) == str(other)
        
    def __lt__(self, other):
        return str(self) < str(other)
        
    def expand(self,p):
        """ étend un noeud avec ces fils
            pour un probleme de taquin p donné
            """
        nouveaux_fils = [Noeud(s,self.g+p.cost(self.etat,s),self) for s in p.successeurs(self.etat)]
        return nouveaux_fils
        
    def expandNext(self,p,k):
        """ étend un noeud unique, le k-ième fils du noeud n
            ou liste vide si plus de noeud à étendre
            """
        nouveaux_fils = self.expand(p)
        if len(nouveaux_fils)<k: 
            return []
        else: 
            return self.expand(p)[k-1]
            
    def chemin(self, p):
        n = self
        c = []
        while n != None:
            c.append(n)
            n = n.pere
        return list(reversed(c))
    
    def trace(self,p):
        """ affiche tous les ancetres du noeud
            """
        n = self
        c=0
        while n!=None :
            print (n)
            n = n.pere
            c+=1
        print ("Nombre d'étapes de la solution:", c-1)
        return




def astar(p,verbose=False,stepwise=False):
    """ Application de l'algorithme a-star
        sur un probleme donné
        """
        
    startTime = time.time()
    nodeInit = Noeud(p.init,0,None)
    frontiere = [(nodeInit.g+p.h_value(nodeInit.etat,p.but),nodeInit)] 
    reserve = {}
    bestNoeud = nodeInit
    
    while frontiere != [] and not p.estBut(bestNoeud.etat):              
        (min_f,bestNoeud) = heapq.heappop(frontiere)     
        
        if p.immatriculation(bestNoeud.etat) not in reserve:            
            reserve[p.immatriculation(bestNoeud.etat)] = bestNoeud.g #maj de reserve
            nouveauxNoeuds = bestNoeud.expand(p)
            for n in nouveauxNoeuds:
                f = n.g+p.h_value(n.etat,p.but)
                heapq.heappush(frontiere, (f,n))

    # Un noeud en réserve peut revenir dans la frontière        
        
        stop_stepwise=""
        if stepwise==True:
            stop_stepwise = input("Press Enter to continue (s to stop)...")
            print ("best", min_f, "\n", bestNoeud)
            print ("Frontière: \n", frontiere)
            print ("Réserve:", reserve)
            if stop_stepwise=="s":
                stepwise=False
            
    # Mode verbose            
    # Affichage des statistiques (approximatives) de recherche   
    if verbose:
        print ("=------------------------------=")
        print ("Nombre de noeuds explorés", len(reserve))
        c=0
        for (f,n) in frontiere:
            if p.immatriculation(n.etat) not in reserve:
                c+=1
        print ("Nombre de noeuds de la frontière", c)
        print ("Nombre de noeuds en mémoire:", c + len(reserve))
        print ("temps de calcul:", time.time() - startTime)
        print ("=------------------------------=")

    return bestNoeud.chemin(p)
