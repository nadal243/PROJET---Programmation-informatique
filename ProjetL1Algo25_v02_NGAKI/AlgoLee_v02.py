# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 00:36:46 2025

@author: Ibisc-Loup
"""

import numpy as np

#Version de l'algorithme de Lee adaptée au projet
def calculLaby(pLaby,pValsDisponibles,xDepart,yDepart,xArrivee,yArrivee):
    """
    Obj : effectue le calcul des distances en parcourant le tableau
    - strategie consiste à chercher les cases tagguees au bon indice et a modifier leur voisin
    Arg1 pLaby : Matrice du labyrinthe
    Arg2 pValsDisponibles : liste des types de valeurs que le chemin peut emprunter
    Arg3&4 xDepart,yDepart : coordonnées de la position initiale
    Arg5&6 xArrivee,yArrivee : coordonnées de la position finale
    Ret : direction à prendre Haut=[0,1] / Bas=[0,-1] / Gauche=[-1,0] / Droite=[0,1]
    """
    # faire un nouveau tableau initialiser avec une valeur maximum pour assurer que le bon fonctionnement du min
    defaultVal = len(pLaby[0])*len(pLaby)
    distance=np.copy(pLaby)
    for i in range(len(pLaby)):
        for j in range(len(pLaby[0])) :
            distance[i][j]=defaultVal
    distance[xDepart][yDepart]=0#Position initiale

    # voisins connexite 4
    voisins=[[0,1],[0,-1],[1,0],[-1,0]]

    # tant que non fini
    fini = False
    indice = 0

    while (not fini) :
        # remet fini a vrai
        fini = True

        for i in range(1,len(pLaby)-1):
            for j in range(1,len(pLaby[0])-1):
                # si case est taggue avec le bon indice

                if distance[i][j]==indice:
                    # pour chaque voisin
                    for v in voisins:
                        # coordonnes du voisin
                        voisinX=i+v[0]
                        voisinY=j+v[1]
                        # si case a une valeur autorisée
                        # si case non calculée
                        #Les coordonnées de la matrice pLaby sont inversés car la matrice est utilisée autrement
                        if (pLaby[voisinY][voisinX] in pValsDisponibles) and distance[voisinX][voisinY]==defaultVal:
                            # tague
                            distance[voisinX][voisinY] = indice +1
                            # fini est faux
                            fini = False
                        
        # decale indice
        indice = indice  +1

    ###################################
    # Recherche de la bonne direction #
    ###################################
    x=xArrivee
    y=yArrivee
    mini=defaultVal
    voisinMin =()
    # pour chaque voisin
    for voisin in voisins :
        # calcule case voisine
        vx = x + voisin[0]
        vy = y + voisin[1]
        # si meilleure
        if distance[vx][vy] < mini :
            mini = distance[vx][vy]
            voisinMin = voisin

    # on se place au depart
    # fin retourne chemin
    return voisinMin
