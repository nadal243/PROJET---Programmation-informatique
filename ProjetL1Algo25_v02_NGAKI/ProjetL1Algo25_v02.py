#!/usr/bin/env python
# -*- coding: utf-8 -*-
#v2
#2.1 Bug Restart > Suppression des NappeHydro
#2.2 Bug Navigation OP
#afficher_classement_final(budgetOM)  # Si budgetOM est le budget fina
"""
Projet : sujet 11  ->  Eco guerrir
Auteur : NGAKI MUPATI NADAL
Date de création :
Description : Un type de navire n’appartenant à aucun des 2 organismes aura les caractéristiques suivantes :  
    a) Déplacements aléatoires mais plus rapides 
    b) Collision avec le navire OP  fera disparaitre son chargement. 

"""

#Modules importés
from tkinter import *
import random
import math
import numpy as np

# ----------------------------------------------------------------
# Variables globales
# ----------------------------------------------------------------

#Liste des entites mobiles (ID)
entitesMobiles=[]
#Liste des entités mobiles
typesEntiteMobile=[]
TYPE_ORGA_MARITIME=1
TYPE_ORGA_PETROL=5
TYPE_NAPPE_HYDRO=6
NAVIRE_PIRATE=4    # initialisation de mon navire pirate 
#A intégrer
etats_chargement=[]
ETAT_CHARGEMENT_MIN=0
ETAT_CHARGEMENT_MAX=100
#DEGAT_ORGA_PETROL=10



#Coordonnées initiales de tous les navires
coord_iEntitesMobiles_Init=[]#Abscisse Navires
coord_jEntitesMobiles_Init=[]#Ordonnée Navires

#Coordonnées actuelles de tous les navires
coord_iEntitesMobiles=[]#Abscisse Navires >> nombre réél à convertir en entier pour utiliser en coordonnées matricielle
coord_jEntitesMobiles=[]#Ordonnée Navires

#temps pour le chronometre 

duree_partie = 0  # Temps écoulé en secondes
chrono_actif = False  # Indique si le chronomètre est en cours


#Vitesses actuelles de tous les navires
vitX=[]
vitY=[]
#Distance incrémentée à chaque déplacement
VIT_MAX_OrgaMaritime = 0.04
VIT_MAX_OrgaPetrole = 0.03
VIT_MAX_NAVIRE_PIRATE = 0.06

### Legende des Matrices de décor ###
#Zones naviguables
ZN=10#Zone maritime neutre : non explitée/non protégée
ZP=11#Zone maritime protégée
BP=20#Base portuaire pétrolière
PP=30#Plateforme pétrolière
BM=40#Base portuaire OMI
CG=60     #coin gauche haut 
CD=70     #coin droite haut
CDh=80    #coin droite bas 
CGh=90    #coin gache bas
CH=100    #cote haut 
CB=110    #cote bas
cG=120    #cote gauche
cD=140    #cote droite 

#Zones non naviguable
ZT=50#Zone terrestre




#Matrice de la carte du Niveau 1
matValCarteN1 = [
    [CG, CH, CH, CH, CH, CH, CH, CH, CH, CH, CH, CH, CH, CH, CH, CH, CD],
    [cG, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, cD],
    [cG, ZN, CG, CH, CD, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, cD],
    [cG, ZN, cG, ZT, cD, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, cD],
    [cG, ZN, CGh, CB, CDh, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, PP, ZN, ZN, cD],
    [cG, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, cD],
    [cG, BM, ZP, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, cD],
    [cG, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, cD],
    [cG, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, BP, cD],
    [cG, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, cD],
    [cG, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, cD],
    [cG, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, cD],
    [cG, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, cD],
    [cG, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, cD],
    [cG, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, cD],
    [cG, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, ZN, cD],
    [CGh, CB, CB, CB, CB, CB, CB, CB, CB, CB, CB, CB, CB, CB, CB, CB, CDh]
]



matValCarteN1_initial=np.copy(matValCarteN1)#Copie pout conservation des valeurs initiales durant la simulation

#Dimension de chaque case en pixel
LARG_CASE=40#Largeur
HAUT_CASE=40#Hauteur

#Dimensions
LARG_CANVAS = len(matValCarteN1)*LARG_CASE
HAUT_CANVAS = len(matValCarteN1[0])*HAUT_CASE

#Etat des animations et déplacements
etat_actif_depl_anim = False

#Demande d'arrêt
dde_arret = False

#Gestion du budget
budgetOM=budgetOM_INIT=5000
budgetOP=budgetOP_INIT=5000
tarifSANCTION=500#Tarif d'une sanction en cas de décrouverte d'une nappe
tarifVENTE=100#Tarif d'une vente de pétrole
tarifTRAITEMENT=100#Tarif de traitement de déchets
tarifDEGAT=500#Tarif de destruction d'une zone protégée
FICHIER_BUDGET = "budget.txt"  # declaration du budget comme fichier txt

#durée de simulation
dureeSimulation=0#en s
tpsRafraichissement=0.1#en s
# dureePP_Initiale=10#en s
dureePP_Initiale=20#en s
# dureePP=10#en s
dureePP=20#en s
# dureeZP_Initiale=10#en
dureeZP_Initiale=20#en s
#dureeZP=10#en s
dureeZP=20#en s


# ----------------------------------------------------------------
# Fonctions
# ----------------------------------------------------------------
def charger_record():
    """Charge le record (budget max) depuis le fichier."""
    
    fichier = open(FICHIER_BUDGET, "r")
    lignes = fichier.readlines()
    fichier.close()
        
    if lignes:
        return max(map(float, lignes))  # Trouver le budget max
    

def sauvegarder_budget(budget):
    """Ajoute un budget au fichier et met à jour l'affichage."""
    fichier = open(FICHIER_BUDGET, "a")  # Ouvrir en mode ajout
    fichier.write(f"{budget}\n")
    fichier.close()

def afficher_budget_et_record():
    """Affiche le budget et le record sur l'interface."""
    record = charger_record()
    lblBudgetRecord.config(text=f"Record : {record}")
def charger_tous_les_budgets():
    """Charge tous les budgets enregistrés et les trie du plus grand au plus petit."""

    fichier = open(FICHIER_BUDGET, "r")
    lignes = fichier.readlines()
    fichier.close()

    budgets = list(map(float, lignes))  # Convertir en nombres
    budgets.sort(reverse=True)  # Trier du plus grand au plus petit
    return budgets

def afficher_classement_final(budget_final):
    """Affiche un message de classement basé sur le budget final."""
    budgets = charger_tous_les_budgets()  # Charger tous les budgets classés

    if not budgets:  # Si aucun budget n'est enregistré
        message = "C'est votre premier budget enregistré !"
    elif budget_final == budgets[0]:  # Si c'est le record
        message = "🎉 Nouveau Record ! Félicitations ! 🎉"
    else:
        try:
            position = budgets.index(budget_final) + 1  # Trouver la position
            message = f"🏅 {position}ème Meilleur Budget !"
        except ValueError:
            message = "Budget non trouvé dans le classement."

    lblMessage.config(text=message)  # Mettre à jour l'affichage du message

    
"""
Obj: Tirage aléatoire d'un emplacement d'un type parmi ceux la liste passé en argument
Les zones en bordure ne sont pas prises en compte
Arg : liste des types zones qui nous interessent
Retour : liste de 2 élements : Coordonnées (en matriciel et non en pixel)

"""
def getCoordAleatoire(pTypesZones,pVoisinsEgalement=False,pBordure=0):

    dispo=False
    while (not dispo):
        i=random.randint(pBordure,len(matValCarteN1)-1-pBordure)
        j=random.randint(pBordure,len(matValCarteN1[0])-1-pBordure)
  
        if (pVoisinsEgalement):
            if(len(voisinsDisponibles(matValCarteN1,pTypesZones,j,i))==8):
                dispo=(matValCarteN1[j][i] in pTypesZones)
        else:
            dispo=(matValCarteN1[j][i] in pTypesZones)

    return [i,j]

# creation d'une fonction pour la mise à jour du chronometre 

def miseAJourDuree():
    global duree_partie, chrono_actif

    if chrono_actif:  # Vérifie si le chronomètre est actif
        duree_partie += 1  # Incrémente le temps de jeu
        lblDureePartie.config(text=f"Durée : {duree_partie}s")  # Met à jour l'affichage
        fen_princ.after(1000, miseAJourDuree)  # Rappelle la fonction après 1 seconde


"""
Obj : Recherche les coordonnées d'une zone unique et forcement présente
Arg : type de zone unique recherchée
Retour : Coordonnées trouvées
"""
def getCelluleZoneUnique(pTYPE_ZONE):
    dispo=False
    i=0
    j=0
    while (not dispo):
        if (matValCarteN1[j][i]==pTYPE_ZONE):
            dispo=True
        else:
            j+=1
            if j>=(len(matValCarteN1)):
                j=0
                i+=1            
                if i>=(len(matValCarteN1[0])):
                    dispo=True#Rien n'a été trouvé             

    return [i,j]

"""
Obj: Convertion des coordonnées réélles en coordonnées entières pour consulter la matrice
Permet ainsi de connaître le type d'item qui occupe la case occupé par le navire
Retour : liste de 2 élements : Coordonnées (en matriciel et non en pixel)

"""
def getCelluleEntiteMobile(pNoEntiteMobile):
    return [round(coord_iEntitesMobiles[pNoEntiteMobile]),round(coord_jEntitesMobiles[pNoEntiteMobile])]

"""
Obj: Convertir les indices de tableau en coordonnées pixel 
Paramètres : indices du tableau niveau
Retour : liste des 2 coordonnées en pixel 
"""
def getConvertCoordNiveauEnCoordPixels(i,j):
    x=LARG_CASE*i
    y=HAUT_CASE*j
    return [x,y]

"""
Obj: Convertir les coordonnées pixel en indices de tableau niveau
Paramètres : coordonnées pixel
Retour : liste des 2 indices du tableau matValCarteN1
"""
def getConvertCoordPixelsEnCoordNiveau(x,y):
    i=int(x/(LARG_CASE-(x%LARG_CASE)))
    j=int(y/(HAUT_CASE-(y%HAUT_CASE)))
    return [i,j]

"""
Obj: Convertir les coordonnées pixel en indices de tableau niveau
Paramètres : image et nouvelles coordonnées en pixel
"""
def deplacerImage(im,newX,newY):
    global gestionCanvas
    gestionCanvas.coords(im,newX,newY,
                         newX+LARG_CASE,newY+HAUT_CASE)

"""
Obj: suppression de la nappe hydrocarbure avec la touche n

"""
 
def suppression_des_nappes_hydocarbures ():
    global budgetOM, budgetOP
    for i in range(len(entitesMobiles)-1, -1, -1): #pour un parcours inversé afin d'éviter les problemes de suppresion 
        if typesEntiteMobile[i]==TYPE_NAPPE_HYDRO and etats_chargement[i]==ETAT_CHARGEMENT_MAX:
            #suppression de l'image 
            gestionCanvas.delete(entitesMobiles[i])
            #suppresio des données reletives aux nappes 
            coord_iEntitesMobiles_Init.pop(i)
            coord_jEntitesMobiles_Init.pop(i)
            coord_iEntitesMobiles.pop(i)
            coord_jEntitesMobiles.pop(i)
            vitX.pop(i)
            vitY.pop(i)
            entitesMobiles.pop(i)
            typesEntiteMobile.pop(i)
            etats_chargement.pop(i)
            budgetOM+=tarifTRAITEMENT  #augmentation du budget de OM
            budgetOP-=tarifSANCTION    #reduction du budget de OP
            lblBudgetOM.config(text="budget OM :"+ str(budgetOM))
            lblBudgetOP.config(text="budget OP :"+ str(budgetOP))
            print("la suppression de la nappe a été un succes !")
            
            break  # pour sortir apres avoir supprimé une nappe hydrocarbure 
"""
Obj:Ajoute une nouvelle zone protégée sur une zone neutre (ZN).
"""
def ajout_de_nouvelles_zones_protegées():
    global matValCarteN1
    newCoordZP = getCoordAleatoire([ZN], True, 1)
    matValCarteN1[newCoordZP[1]][newCoordZP[0]] = ZP  # Mettre à jour la matrice
    gestionCanvas.itemconfig(matImgCarteN1[newCoordZP[1]][newCoordZP[0]], image=imgZP)  # Mise à jour de l'affichage
    print(" Nouvelle zone protégée ajoutée !")  # Message pour suivi

"""
Obj:Déplace la plateforme pétrolière vers une nouvelle zone neutre.
"""
def deplacement_de_la_plateforme_petroliere():
    global matValCarteN1
    oldCoordPP = getCelluleZoneUnique(PP)
    newCoordPP = getCoordAleatoire([ZN], True, 1)
    
    # Mise à jour des matrices
    matValCarteN1[newCoordPP[1]][newCoordPP[0]] = PP
    matValCarteN1[oldCoordPP[1]][oldCoordPP[0]] = ZN
    
    # Mise à jour de l'affichage
    gestionCanvas.itemconfig(matImgCarteN1[oldCoordPP[1]][oldCoordPP[0]], image=imgZN)
    gestionCanvas.itemconfig(matImgCarteN1[newCoordPP[1]][newCoordPP[0]], image=imgPP)
    print("Plateforme pétrolière déplacée avec succès !")  # Message pour suivi
            

"""
Obj: Gestion des évènements du clavier

"""
def evenements(event):
    if event.keysym=="Up":
        pilotage(0,0,-VIT_MAX_OrgaMaritime)# demarrage(0,-VIT_MAX_OrgaMaritime)#,btnHaut)
    elif event.keysym=="Down":
        pilotage(0,0,VIT_MAX_OrgaMaritime)#,btnBas)
    elif event.keysym=="Left":
        pilotage(0,-VIT_MAX_OrgaMaritime,0)#,btnGauche)
    elif event.keysym=="Right":
        pilotage(0,VIT_MAX_OrgaMaritime,0)#,btnDroite)
    elif event.keysym == "n":
        suppression_des_nappes_hydocarbures()
    elif event.keysym == "v":
        ajout_de_nouvelles_zones_protegées()
    elif event.keysym == "p":
        deplacement_de_la_plateforme_petroliere()
        
    
    if event.keysym=="Escape":
        arret()
    elif event.keysym=="space":
        depart()
"""
Obj: suppression de la nappe hydrocarbure avec la touche n

"""
 

    

"""
Obj: Instanciation d'une nouvelle entité mobile (ex : navire, nappe hydrocarbure,etc..)
Param : Type d'entité mobile
"""
def creationEntiteMobile(pTypeEntiteMobile):
    global vitX,vitY,coord_iEntitesMobiles_Init,coord_jEntitesMobiles_Init,entitesMobiles
    global typesEntiteMobile,etats_chargement,gestionCanvas, posInitEntiteMobile
    
    if (pTypeEntiteMobile==TYPE_ORGA_MARITIME):
        posInitEntiteMobile=getCelluleZoneUnique(BM)#voisinsDisponibles(matValCarteN1,[ZT],getCelluleZoneUnique(BM)[0],getCelluleZoneUnique(BM)[1])[0]
    elif (pTypeEntiteMobile==TYPE_ORGA_PETROL):
        posInitEntiteMobile=getCelluleZoneUnique(BP)
    elif (pTypeEntiteMobile==TYPE_NAPPE_HYDRO):
        posInitEntiteMobile=getCelluleZoneUnique(PP)
    elif (pTypeEntiteMobile == NAVIRE_PIRATE):        # creation navire pirate 
        posInitEntiteMobile = getCoordAleatoire([ZN])  # Choisir une zone océanique
    coord_i_EntiteMobile=posInitEntiteMobile[0]
    coord_j_EntiteMobile=posInitEntiteMobile[1]
    coord_iEntitesMobiles_Init.append(coord_i_EntiteMobile)
    coord_jEntitesMobiles_Init.append(coord_j_EntiteMobile)
    coord_iEntitesMobiles.append(coord_i_EntiteMobile)
    coord_jEntitesMobiles.append(coord_j_EntiteMobile)

    vitX.append(0)
    vitY.append(0)
    
    coordPixel=getConvertCoordNiveauEnCoordPixels(posInitEntiteMobile[0],posInitEntiteMobile[1])
    
    #matValCarteN1[coord_j_EntiteMobile][coord_i_EntiteMobile]=pTypeEntiteMobile
    if (pTypeEntiteMobile==TYPE_ORGA_MARITIME):
        entitesMobiles.append(gestionCanvas.create_image(coordPixel[0],coordPixel[1], image=imgBateauOMempty,anchor=NW))
        etats_chargement.append(ETAT_CHARGEMENT_MIN)
        gestionCanvas.tag_raise(entitesMobiles[-1])
    elif (pTypeEntiteMobile==TYPE_ORGA_PETROL):
        entitesMobiles.append(gestionCanvas.create_image(coordPixel[0],coordPixel[1], image=imgBateauOPempty,anchor=NW))
        etats_chargement.append(ETAT_CHARGEMENT_MIN)
        gestionCanvas.tag_raise(entitesMobiles[-1])
    elif (pTypeEntiteMobile==TYPE_NAPPE_HYDRO):
        entitesMobiles.append(gestionCanvas.create_image(coordPixel[0],coordPixel[1], image=imgZH,anchor=NW))
        etats_chargement.append(ETAT_CHARGEMENT_MAX)
    elif (pTypeEntiteMobile==NAVIRE_PIRATE):
        entitesMobiles.append(gestionCanvas.create_image(coordPixel[0],coordPixel[1], image=imgNAVIREPIRATE,anchor=NW))
        etats_chargement.append(ETAT_CHARGEMENT_MIN)
        gestionCanvas.tag_raise(entitesMobiles[-1])
    
    typesEntiteMobile.append(pTypeEntiteMobile)
    # if pTypeEntiteMobile == NAVIRE_PIRATE:
    #     directions = [
    #     (VIT_MAX_NAVIRE_PIRATE, 0), (-VIT_MAX_NAVIRE_PIRATE, 0), 
    #     (0, VIT_MAX_NAVIRE_PIRATE), (0, -VIT_MAX_NAVIRE_PIRATE)]
    #     vitX[-1], vitY[-1] = random.choice(directions)


"""
Obj: Démarrage des déplacements des entités mobiles
Param :
    pVitesseX : Vitesse demandée par le joueur sur l'axe des abcisses
    pVitesseY : Vitesse demandée par le joueur sur l'axe des ordonnées
    pBtn : Bouton utilisé dont l'apparence doit mise à jour
"""
def pilotage(pNoEntiteMobile,pVitesseX,pVitesseY):
    global dde_arret,etat_actif_depl_anim,vitX,vitY
    
    if etat_actif_depl_anim == True:
        vitX[pNoEntiteMobile]=pVitesseX
        vitY[pNoEntiteMobile]=pVitesseY

"""
Obj: Appel récursif des déplacements de toutes les entités mobiles
Basculer la valeur de dde_arret à True pour stopper les déplacements
"""
def gestion_deplacements():

    global etat_actif_depl_anim, dde_arret,dureeSimulation
    global dureePP,dureeZP,imgCarteLigne,gestionCanvas #,noEntiteMobile
    
    # if typesEntiteMobile[noEntiteMobile] == NAVIRE_PIRATE:
    #     chgtDirectionOP(noEntiteMobile)
    
# pour arreter toutes les entites mobiles
    if (etat_actif_depl_anim):
        for noEntiteMobile in range(len(entitesMobiles)):
            deplacement(noEntiteMobile)#,typesEntiteMobile[i])
            if typesEntiteMobile[noEntiteMobile] == NAVIRE_PIRATE:
                chgtDirectionOP(noEntiteMobile)


        #Gestion des évolutions des zones PP et ZP
        dureePP-=tpsRafraichissement
        dureeZP-=tpsRafraichissement
        if (dureePP<0):#la PP a terminé son exploitation, une nouvelle doit être construite
            dureePP=dureePP_Initiale
            #déplacer la PP
            oldCoordPP=getCelluleZoneUnique(PP)
            newCoordPP=getCoordAleatoire([ZN],True,1)
            matValCarteN1[newCoordPP[1]][newCoordPP[0]]=PP
            matValCarteN1[oldCoordPP[1]][oldCoordPP[0]]=ZN
            gestionCanvas.itemconfig(matImgCarteN1[oldCoordPP[1]][oldCoordPP[0]],image = imgZN)
            gestionCanvas.itemconfig(matImgCarteN1[newCoordPP[1]][newCoordPP[0]],image = imgPP)
        if (dureeZP<0):#la ZP est suffisemment développée et une nouvelle peut être aménagée
            dureeZP=dureeZP_Initiale
            #déplacer la ZP
            newCoordZP=getCoordAleatoire([ZN],True,1)
            matValCarteN1[newCoordZP[1]][newCoordZP[0]]=ZP
            gestionCanvas.itemconfig(matImgCarteN1[newCoordZP[1]][newCoordZP[0]],image = imgZP)
    
    
    if dde_arret == False :#Tant que le simulateur ne doit pas être arrêté
        dureeSimulation+=tpsRafraichissement

        fen_princ.after(int(1000*tpsRafraichissement), gestion_deplacements)#Patienter 100ms afin d'appeler à nouveau cette même fonction (récursivité)
    else:
        dde_arret = False #Arrêt pris en compte et réinitialisé
        etat_actif_depl_anim = False #Animation désactivée
        
"""
Obj: Gestion de la logique de déplacement des ennemis
Param :
    pNoEntiteMobile : Identifiant du navire concerné
"""
def chgtDirectionOP(pNoEntiteMobile):
    global vitX, vitY, typesEntiteMobile
    
    if typesEntiteMobile[pNoEntiteMobile] == NAVIRE_PIRATE:
        direction = random.randint(1,100)
        if (direction<2):     #pour un changement de direction plus nette et normale
            # Mouvement aléatoire pour le navire pirate
            directions = [
                (VIT_MAX_NAVIRE_PIRATE, 0), (-VIT_MAX_NAVIRE_PIRATE, 0), 
                (0, VIT_MAX_NAVIRE_PIRATE), (0, -VIT_MAX_NAVIRE_PIRATE)
            ]
            vitX[pNoEntiteMobile], vitY[pNoEntiteMobile] = random.choice(directions)
    
    elif typesEntiteMobile[pNoEntiteMobile] == TYPE_ORGA_PETROL:
        # Comportement déjà existant pour l'OP
        if etats_chargement[pNoEntiteMobile] == ETAT_CHARGEMENT_MAX:
            coordCible = getCelluleZoneUnique(BP)
        else:
            coordCible = getCelluleZoneUnique(PP)

        vitX[pNoEntiteMobile], vitY[pNoEntiteMobile] = 0, 0

        if round(coord_iEntitesMobiles[pNoEntiteMobile]) > coordCible[0]:
            vitX[pNoEntiteMobile] = -VIT_MAX_OrgaPetrole
        elif round(coord_iEntitesMobiles[pNoEntiteMobile]) < coordCible[0]:
            vitX[pNoEntiteMobile] = VIT_MAX_OrgaPetrole
        elif round(coord_jEntitesMobiles[pNoEntiteMobile]) > coordCible[1]:
            vitY[pNoEntiteMobile] = -VIT_MAX_OrgaPetrole
        elif round(coord_jEntitesMobiles[pNoEntiteMobile]) < coordCible[1]:
            vitY[pNoEntiteMobile] = VIT_MAX_OrgaPetrole
    else:
         
        direction = random.randint(1,100)
     
        #if (vitX[pNoEntiteMobile]==0 and vitY[pNoEntiteMobile]==0): #Changement de direction si nous sommes à l'arrêt
        if direction <= 2 :#25% de chance qu'il parte à droite
            vitX[pNoEntiteMobile] = VIT_MAX_OrgaPetrole
            vitY[pNoEntiteMobile] = 0

        elif direction <= 4 :#25% de chance qu'il parte à gauche
            vitX[pNoEntiteMobile] = -VIT_MAX_OrgaPetrole
            vitY[pNoEntiteMobile] = 0

        elif direction <= 6 :#25% de chance qu'il parte en bas
            vitX[pNoEntiteMobile] = 0
            vitY[pNoEntiteMobile] = VIT_MAX_OrgaPetrole

        elif direction <= 8:# de 75% et 100% inclus
            vitX[pNoEntiteMobile] = 0#25% de chance qu'il parte en haut
            vitY[pNoEntiteMobile] = -VIT_MAX_OrgaPetrole


"""
Obj: Gestion des déplacements de chaque navire
Param :
    pNoEntiteMobile : Identifiant du navire concerné

"""
def deplacement(pNoEntiteMobile):
    global entitesMobiles, vitX, vitY,coord_iEntitesMobiles,typesEntiteMobile,etats_chargement,budgetOM,budgetOP
    
    
    #2.2 Correction Naviguation OP ++
    # if typesEntiteMobile[pNoEntiteMobile] == NAVIRE_PIRATE:
    #     if random.random() < 0.1:  # 10% de chance de changer de direction à chaque déplacement
    #         chgtDirectionOP(pNoEntiteMobile)
    if typesEntiteMobile[pNoEntiteMobile] == NAVIRE_PIRATE:
        if vitX[pNoEntiteMobile] == 0 and vitY[pNoEntiteMobile] == 0:  # S'il est immobile, forcer un changement
            chgtDirectionOP(pNoEntiteMobile)
        elif random.random() < 0.1:  # Sinon, il a 10% de chance de changer de direction
            chgtDirectionOP(pNoEntiteMobile)


    #Relancer les navires ennemis
    if (typesEntiteMobile[pNoEntiteMobile]!=TYPE_ORGA_MARITIME):
        chgtDirectionOP(pNoEntiteMobile)
    #2.2 Correction Naviguation OP--
    
    
    #Cas de changement d'axe de direction > Réaligner l'ancien
    if (vitX[pNoEntiteMobile]!=0):
        coord_jEntitesMobiles[pNoEntiteMobile]=round(coord_jEntitesMobiles[pNoEntiteMobile])
    else:#vitY!=0
        coord_iEntitesMobiles[pNoEntiteMobile]=round(coord_iEntitesMobiles[pNoEntiteMobile])
    
    #Incrémentation des coordonnées en fonction de la vitesse du navire
    coord_iEntitesMobiles[pNoEntiteMobile]+=vitX[pNoEntiteMobile]
    coord_jEntitesMobiles[pNoEntiteMobile]+=vitY[pNoEntiteMobile]    
    
    #identification des coordonnées de la cellule sur laquelle le navire s'engage 
    if (vitX[pNoEntiteMobile]>0 or vitY[pNoEntiteMobile]>0):
        coord_iEntiteMobile_matCarte=math.ceil(coord_iEntitesMobiles[pNoEntiteMobile])
        coord_jEntiteMobile_matCarte=math.ceil(coord_jEntitesMobiles[pNoEntiteMobile])
    else:
        coord_iEntiteMobile_matCarte=math.floor(coord_iEntitesMobiles[pNoEntiteMobile])
        coord_jEntiteMobile_matCarte=math.floor(coord_jEntitesMobiles[pNoEntiteMobile])
    
    #identification du type de décor présent sur cette cellule
    typeCarte=(matValCarteN1[coord_jEntiteMobile_matCarte][coord_iEntiteMobile_matCarte])
    
    
    #2.2 Correction Naviguation OP ++
    #Relancer les navires ennemis
    #if (typesEntiteMobile[pNoEntiteMobile]!=TYPE_ORGA_MARITIME):
    #    chgtDirectionOP(pNoEntiteMobile)
    #2.2 Correction Naviguation OP--
    
    if (typeCarte>=ZT):#Cas de collision avec des zones non naviguables
        #Repositionnement du navire
        if (vitX[pNoEntiteMobile]>0):
            coord_iEntitesMobiles[pNoEntiteMobile]=coord_iEntiteMobile_matCarte-1
        elif (vitX[pNoEntiteMobile]<0):
            coord_iEntitesMobiles[pNoEntiteMobile]=coord_iEntiteMobile_matCarte+1
        elif (vitY[pNoEntiteMobile]>0):
            coord_jEntitesMobiles[pNoEntiteMobile]=coord_jEntiteMobile_matCarte-1
        elif (vitY[pNoEntiteMobile]<0):
            coord_jEntitesMobiles[pNoEntiteMobile]=coord_jEntiteMobile_matCarte+1
        
        #Arrêt du navire
        vitX[pNoEntiteMobile]=0
        vitY[pNoEntiteMobile]=0
        
    #Cas de la nappe d'hydrocarbure arrivant dans une zone protégée
    elif (typeCarte==ZP and typesEntiteMobile[pNoEntiteMobile]==TYPE_NAPPE_HYDRO and etats_chargement[pNoEntiteMobile]==ETAT_CHARGEMENT_MAX):
            #Changer le statut de la cible
            matValCarteN1[coord_jEntiteMobile_matCarte][coord_iEntiteMobile_matCarte]=ZN
            #Modifier l'image
            gestionCanvas.itemconfig(matImgCarteN1[coord_jEntiteMobile_matCarte][coord_iEntiteMobile_matCarte], 
                                     image = imgZN)
            #mise à jour du budget            
            budgetOM=int(budgetOM)-tarifDEGAT
            lblBudgetOM.config(text = "Budget OM : "+str(budgetOM))
            sauvegarder_budget(budgetOM) # pour la sauvegarde du budget de OM
            afficher_budget_et_record()
    #Cas de l'arrivée d'un navire de l'OM chargée à son port
    elif (typeCarte==BM and typesEntiteMobile[pNoEntiteMobile]==TYPE_ORGA_MARITIME and etats_chargement[pNoEntiteMobile]==ETAT_CHARGEMENT_MAX):
            #Déchargement du navire de l'OM
            etats_chargement[pNoEntiteMobile]=ETAT_CHARGEMENT_MIN
            gestionCanvas.itemconfig(entitesMobiles[pNoEntiteMobile],image = imgBateauOMempty)
            #incrémentation du budget            
            budgetOM=int(budgetOM)+tarifTRAITEMENT
            lblBudgetOM.config(text = "Budget OM : "+str(budgetOM))
            sauvegarder_budget(budgetOM)  # pour la sauvegarde du budget de OM
            afficher_budget_et_record()

    #Cas de l'arrivée d'un navire de l'OP vide à la plateforme pétrolière
    elif (typeCarte==PP and typesEntiteMobile[pNoEntiteMobile]==TYPE_ORGA_PETROL and etats_chargement[pNoEntiteMobile]==ETAT_CHARGEMENT_MIN):
            #Chargement du navire de l'OP
            etats_chargement[pNoEntiteMobile]=ETAT_CHARGEMENT_MAX
            gestionCanvas.itemconfig(entitesMobiles[pNoEntiteMobile],image = imgBateauOPfull)
            creationEntiteMobile(TYPE_NAPPE_HYDRO)
    #Cas de l'arrivée d'un navire de l'OP chargée à son port
    elif (typeCarte==BP and typesEntiteMobile[pNoEntiteMobile]==TYPE_ORGA_PETROL and etats_chargement[pNoEntiteMobile]==ETAT_CHARGEMENT_MAX):
            #Déchargement du navire de l'OP
            etats_chargement[pNoEntiteMobile]=ETAT_CHARGEMENT_MIN
            gestionCanvas.itemconfig(entitesMobiles[pNoEntiteMobile],image = imgBateauOPempty)
            #incrémentation du budget            
            budgetOP=int(budgetOP)+tarifVENTE
            lblBudgetOP.config(text = "Budget OP : "+str(budgetOP))
            sauvegarder_budget(budgetOP)  # Sauvegarde OP
            afficher_budget_et_record()


    #Recherche de collision entre entites mobiles
    for a in range(0,len(entitesMobiles)):
        #Cas de l'interception de la nappe d'hydrocarbure a par le navire de l'OM pNoEntiteMobile
        if (typesEntiteMobile[pNoEntiteMobile]==TYPE_ORGA_MARITIME and typesEntiteMobile[a]==TYPE_NAPPE_HYDRO):
            if (getCelluleEntiteMobile(a)==getCelluleEntiteMobile(pNoEntiteMobile)):
                if (etats_chargement[pNoEntiteMobile]==ETAT_CHARGEMENT_MIN and etats_chargement[a]==ETAT_CHARGEMENT_MAX):
                    #Changer le statut de la cible
                    matValCarteN1[coord_jEntiteMobile_matCarte][coord_iEntiteMobile_matCarte]=ZN
                    #Disparition de la nappe hydrocarbure
                    etats_chargement[a]=ETAT_CHARGEMENT_MIN
                    vitX[a]=0
                    vitY[a]=0
                    gestionCanvas.itemconfig(entitesMobiles[a],image = imgZN)
                    gestionCanvas.tag_lower(entitesMobiles[a])
                    budgetOP=int(budgetOP)-tarifSANCTION
                    lblBudgetOP.config(text = "Budget OP : "+str(budgetOP))
                    #Chargement du navire de l'OM
                    etats_chargement[pNoEntiteMobile]=ETAT_CHARGEMENT_MAX
                    gestionCanvas.itemconfig(entitesMobiles[pNoEntiteMobile],image = imgBateauOMfull)
                    
    
        #cas de l'interception du navire OP par mon navire pirate 
        elif (typesEntiteMobile[pNoEntiteMobile]==NAVIRE_PIRATE and typesEntiteMobile[a]==TYPE_ORGA_PETROL):
            # Vérification si les deux navires sont dans la même cellule
            if (getCelluleEntiteMobile(a) == getCelluleEntiteMobile(pNoEntiteMobile)):
                # Vérification des états de chargement
                if (etats_chargement[a] == ETAT_CHARGEMENT_MAX):  # Le navire OP était chargé
                    etats_chargement[a] = ETAT_CHARGEMENT_MIN  # Il perd son chargement
                    gestionCanvas.itemconfig(entitesMobiles[a], image=imgBateauOPempty)  # Mise à jour de l'image
                    budgetOP -= tarifSANCTION  # Réduction du budget OP
                    lblBudgetOP.config(text=f"Budget OP : {budgetOP}")  # Mettre à jour l'affichage


    #Potentielle victoire et défaite
    if (typesEntiteMobile[pNoEntiteMobile]==TYPE_ORGA_MARITIME):
        VictoireDefaite()
        
        # pour mon bateau pirate 
    elif (typesEntiteMobile[pNoEntiteMobile]==NAVIRE_PIRATE):
        VictoireDefaite()
    
    #Repositonnement de l'image du navire en fonction de ses nouvelles coordonnées
    gestionCanvas.coords(entitesMobiles[pNoEntiteMobile],coord_iEntitesMobiles[pNoEntiteMobile]*LARG_CASE,coord_jEntitesMobiles[pNoEntiteMobile]*HAUT_CASE)

"""
Obj: Réinitiaisation toutes les positions et les vitesses et arrêt des animations et déplacements
"""
def depart():

    global vitX, vitY,typesEntiteMobile,dde_arret,etat_actif_depl_anim,budgetOM,budgetOP,etats_chargement
    global duree_partie, chrono_actif  # Ajout des variables globales
    

    
    if (etat_actif_depl_anim==False):
        #Annulation de la vitesse en cours
        for i in range (len(vitX)):
            vitX[i]=0
        for i in range (len(vitY)):
            vitY[i]=0
    # Réinitialisation du temps uniquement si la partie n’a pas encore commencé
    if duree_partie == 0:
        duree_partie = 0
        lblDureePartie.config(text="Durée : 0s")  # Réinitialise l'affichage
    
    chrono_actif = True  # Active le chronomètre
    miseAJourDuree()  # Démarre le chrono
            
    for i in range(len(typesEntiteMobile)):
        if typesEntiteMobile[i] == NAVIRE_PIRATE:
            directions = [(VIT_MAX_NAVIRE_PIRATE, 0), (-VIT_MAX_NAVIRE_PIRATE, 0), (0, VIT_MAX_NAVIRE_PIRATE), (0, -VIT_MAX_NAVIRE_PIRATE)]
            vitX[i], vitY[i] = random.choice(directions)  # 🏴‍☠️ Donne une direction aléatoire

        
        #Réinitialisation des états de fonctionnement
        for i in range (len(etats_chargement)):
            if (typesEntiteMobile[i]==TYPE_NAPPE_HYDRO):
                etats_chargement[i]=ETAT_CHARGEMENT_MAX
            else:
                etats_chargement[i]=ETAT_CHARGEMENT_MIN
        #lblEtat.config(text = "Etat : "+str(etats_chargement[0])+"%")
    
        #Arrêt des animations et déplacement
        dde_arret = False
        etat_actif_depl_anim = True

        #2.1 Supression des Zones Nappes Hydro++
        nbNappesHydrocarbures=len(entitesMobiles)-(nbNavireOrgaMaritime+nbNavireOrgaPetroliere+nbNAVIREPIRATE)   #ajout de la variable nbNAVIREPIRATE pour la bon fonctionnement
        for i in range(nbNappesHydrocarbures):
            coord_iEntitesMobiles_Init.pop(-1)
            coord_jEntitesMobiles_Init.pop(-1)
            coord_iEntitesMobiles.pop(-1)
            coord_jEntitesMobiles.pop(-1)
            vitX.pop(-1)
            vitY.pop(-1)
            entitesMobiles.pop(-1)
            
        

        #2.1 Supression des Zones Nappes Hydro--
        #Repositionnement aux valeurs initiales        
        for noEntiteMobile in range(0,len(entitesMobiles)):  
            coord_iEntitesMobiles[noEntiteMobile]=coord_iEntitesMobiles_Init[noEntiteMobile]
            coord_jEntitesMobiles[noEntiteMobile]=coord_jEntitesMobiles_Init[noEntiteMobile]
            gestionCanvas.coords(entitesMobiles[noEntiteMobile],
                                 coord_iEntitesMobiles[noEntiteMobile]*LARG_CASE,
                                 coord_jEntitesMobiles[noEntiteMobile]*HAUT_CASE)
            if (typesEntiteMobile[noEntiteMobile]==TYPE_ORGA_MARITIME):
                gestionCanvas.itemconfig(entitesMobiles[noEntiteMobile],image = imgBateauOMempty)
            elif (typesEntiteMobile[noEntiteMobile]==TYPE_ORGA_PETROL):
                gestionCanvas.itemconfig(entitesMobiles[noEntiteMobile],image = imgBateauOPempty)
            # elif (typesEntiteMobile[noEntiteMobile]==NAVIRE_PIRATE):
            #     chgtDirectionOP(noEntiteMobile)
        
        #initialisation du budget            
        budgetOM=budgetOM_INIT
        budgetOP=budgetOP_INIT
        lblBudgetOM.config(text = "Budget OM : "+str(budgetOM))
        lblBudgetOP.config(text = "Budget OP : "+str(budgetOP))
        #initialisation de message de victoire & défaite
        lblMessage.config(text="")
        
        CreationImagesCarte()
        
        gestion_deplacements()


"""
Obj: Arrêt des animations et déplacements sans repositionner
"""
def arret():
    global dde_arret,etat_actif_depl_anim,chrono_actif
        
    if (etat_actif_depl_anim==True):
        #Mise à jour de la variale globale utilisée dans les déplacements
        dde_arret = True
        etat_actif_depl_anim=False
        chrono_actif = False  # Stopper le chronomètre


"""
Obj: Verification des conditions de Victoire et de Défaite
Dans le cas de victoire comme de défaite, le simulateur sera arrêté et un message mis à jour
"""
def VictoireDefaite():
    global matValCarteN1
    nbZonesDisponibles=0
    for i in range(len(matValCarteN1)):
        for j in range(len(matValCarteN1[i])):
            if (matValCarteN1[j][i]==ZN and (len(voisinsDisponibles(matValCarteN1,[ZN],j,i))==8)):
                nbZonesDisponibles+=1
    if (nbZonesDisponibles==0) or budgetOP < 0 :#Aucune zone disponible ajout ;
        arret()
        lblMessage.config(text="Victoire",fg='#0f0')
        # ajout pour mon chronometre
        chrono_actif = False  # Arrêter le chrono
        
    elif budgetOP<0:    
        arret()
        lblMessage.config(text="Victoire",fg='#0f0')
        chrono_actif = False  # Arrêter le chrono
    elif budgetOM<0:    
        arret()
        lblMessage.config(text="Défaite",fg='#f00')
        chrono_actif = False  # Arrêter le chrono
        
        afficher_classement_final(budgetOM)  # Si budgetOM est le budget final


"""
Obj: Créer ou Recréer les images du décor
"""
def CreationImagesCarte():
    global matValCarteN1,matImgCarteN1
    
    #Suppression de toutes les images de décor déjà présentes (cas de redémarrage)
    for imgCarteLigne in matImgCarteN1:
        for j in imgCarteLigne:
            gestionCanvas.delete(j)
    matImgCarteN1.clear()
    
    #réinitialisation des valeurs de la matrice
    matValCarteN1=np.copy(matValCarteN1_initial)
    
    #Création
    for i in range(len(matValCarteN1)):
        imgCarteLigne=[]
        for j in range(len(matValCarteN1[i])):
            if (matValCarteN1[i][j]==ZN):
                imgCarteLigne.append(gestionCanvas.create_image(j*LARG_CASE, i*HAUT_CASE, image=imgZN,anchor=NW))
            elif (matValCarteN1[i][j]==ZP):
                imgCarteLigne.append(gestionCanvas.create_image(j*LARG_CASE, i*HAUT_CASE, image=imgZP,anchor=NW))
            elif (matValCarteN1[i][j]==ZT):
                imgCarteLigne.append(gestionCanvas.create_image(j*LARG_CASE, i*HAUT_CASE, image=imgZT,anchor=NW))
            elif (matValCarteN1[i][j]==BP):
                imgCarteLigne.append(gestionCanvas.create_image(j*LARG_CASE, i*HAUT_CASE, image=imgBP,anchor=NW))
            elif (matValCarteN1[i][j]==PP):
                imgCarteLigne.append(gestionCanvas.create_image(j*LARG_CASE, i*HAUT_CASE, image=imgPP,anchor=NW))
            elif (matValCarteN1[i][j]==BM):
                imgCarteLigne.append(gestionCanvas.create_image(j*LARG_CASE, i*HAUT_CASE, image=imgBM,anchor=NW))    
            elif (matValCarteN1[i][j]==CG):
                imgCarteLigne.append(gestionCanvas.create_image(j*LARG_CASE, i*HAUT_CASE, image=imgCG,anchor=NW))
            elif (matValCarteN1[i][j]==CD):  
                imgCarteLigne.append(gestionCanvas.create_image(j*LARG_CASE, i*HAUT_CASE, image=imgCD,anchor=NW))
            elif (matValCarteN1[i][j]==CDh):  
                imgCarteLigne.append(gestionCanvas.create_image(j*LARG_CASE, i*HAUT_CASE, image=imgCDh,anchor=NW))
            elif (matValCarteN1[i][j]==CGh):  
                imgCarteLigne.append(gestionCanvas.create_image(j*LARG_CASE, i*HAUT_CASE, image=imgCGh,anchor=NW))
            elif (matValCarteN1[i][j]==CH):  
                imgCarteLigne.append(gestionCanvas.create_image(j*LARG_CASE, i*HAUT_CASE, image=imgCH,anchor=NW))
            elif (matValCarteN1[i][j]==CB):  
                imgCarteLigne.append(gestionCanvas.create_image(j*LARG_CASE, i*HAUT_CASE, image=imgCB,anchor=NW))
            elif (matValCarteN1[i][j]==cG):  
                imgCarteLigne.append(gestionCanvas.create_image(j*LARG_CASE, i*HAUT_CASE, image=imgcG,anchor=NW))
            elif (matValCarteN1[i][j]==cD):  
                 imgCarteLigne.append(gestionCanvas.create_image(j*LARG_CASE, i*HAUT_CASE, image=imgcD,anchor=NW))
            gestionCanvas.tag_lower(imgCarteLigne[-1])#v0.5
        matImgCarteN1.append(imgCarteLigne)
        
#Déterminer les zones naviguables autours de la position actuelle
#Args - pLaby : Matrice de la zone
#Args - pValsObstacles : Liste des valeurs considérées comme non naviguables
#Args - pX,pY : coordonnées de la zone auour l'analyse sera effectuée 
#Retour - Liste des voisins
def voisinsDisponibles(pLaby,pValsDisponibles,pX,pY):

    voisinsDisponibles=[]
    # voisins connexite 8
    voisins=[[0,1],[0,-1],[1,0],[-1,0],[1,1],[-1,1],[-1,-1],[1,-1]]
    for v in voisins:
        # coordonnees du voisin
        voisinX=pX+v[0]
        voisinY=pY+v[1]
        if pLaby[voisinX][voisinY] in pValsDisponibles:
            voisinsDisponibles.append([voisinX,voisinY])
            
    return voisinsDisponibles
    
# ----------------------------------------------------------------
# Corps du programme
# ----------------------------------------------------------------

#Paramétrage de la fenêtre principale
fen_princ = Tk()
fen_princ.title("OCEAN WAR L1 SPI")
fen_princ.geometry("900x700")#Dimensions de la fenêtre
fen_princ.bind("<Key>",evenements)#Définition de la fonction de gestion des évènements clavier

#Paramétrage du Canvas
gestionCanvas = Canvas(fen_princ, width=LARG_CANVAS, height=HAUT_CANVAS, bg='ivory', bd=0, highlightthickness=0)
gestionCanvas.grid(row=0,column=0, padx=10,pady=10)

#Affichage des différents types de zone
imgZN=PhotoImage(file = ("img/ocean40.gif"),master=fen_princ)
imgZP=PhotoImage(file = ("img/protection40.gif"),master=fen_princ)
imgZT=PhotoImage(file = ("img/terrainCC40.gif"),master=fen_princ)
imgBP=PhotoImage(file = ("img/port40red.gif"),master=fen_princ)
imgPP=PhotoImage(file = ("img/platform40.gif"),master=fen_princ)
imgBM=PhotoImage(file = ("img/port40green.gif"),master=fen_princ)
imgCG=PhotoImage(file = ("img/terrainHG40.gif"),master=fen_princ) #image pour la cote gauche 
imgCD=PhotoImage(file = ("img/terrainHD40.gif"),master=fen_princ) #image pour le cote droit
imgCGh=PhotoImage(file = ("img/terrainBG40.gif"),master=fen_princ) #image pour le coin gauche bas
imgCDh=PhotoImage(file = ("img/terrainBD40.gif"),master=fen_princ) #image pour le coin droite bas
imgCH=PhotoImage(file = ("img/terrainCH40.gif"),master=fen_princ) #image pour le cote haut
imgCB=PhotoImage(file = ("img/terrainCB40.gif"),master=fen_princ) #image pour le cote bas
imgcG=PhotoImage(file = ("img/terrainCG40.gif"),master=fen_princ) #image pour le coin gauche haut
imgcD=PhotoImage(file = ("img/terrainCD40.gif"),master=fen_princ) #image pour le coin droite haut
matImgCarteN1 = []

#Création et positionnement des images du décor en fonction des valeurs de matValCarteN1
CreationImagesCarte()

#Images utilisées pour l'affichage des navires
imgBateauOMfull=PhotoImage(file = ("img/bateauOMI40full.gif"),master=fen_princ)
imgBateauOMempty=PhotoImage(file = ("img/bateauOMI40empty.gif"),master=fen_princ)
imgZH=PhotoImage(file = ("img/hydrocarbure40a.gif"),master=fen_princ)
imgBateauOPfull=PhotoImage(file = ("img/bateauOPEP40full.gif"),master=fen_princ)
imgBateauOPempty=PhotoImage(file = ("img/bateauOPEP40empty.gif"),master=fen_princ)
imgNAVIREPIRATE=PhotoImage(file = ("img/ecoboat40.gif"),master=fen_princ)  #image pour mon navire pirate

#Création des navires de l'OMI
nbNavireOrgaMaritime=1
for i in range(nbNavireOrgaMaritime):
    creationEntiteMobile(TYPE_ORGA_MARITIME)
    
#creation de mon navire 
nbNAVIREPIRATE=5         # je crée 5 navires pirates pour augmenter l'efficacité
for i in range(nbNAVIREPIRATE):
    creationEntiteMobile(NAVIRE_PIRATE)

#Création des navires de l'OP
nbNavireOrgaPetroliere=1
for i in range(nbNavireOrgaPetroliere):
    creationEntiteMobile(TYPE_ORGA_PETROL)

#Création des nappes hydrocarbures 
nbNappesHydrocarbures=1
for i in range(nbNappesHydrocarbures):
    creationEntiteMobile(TYPE_NAPPE_HYDRO)
    


#Zone dédiée aux boutons
zoneBtn = Frame(fen_princ)
zoneBtn.grid(row=0,column=1,ipadx=5)
  
#Boutons d'arrêt et de réinitialisation
lblMessage = Label(zoneBtn, text="")
Font_tuple = ("Comic Sans MS", 20, "bold")  
lblMessage.configure(font = Font_tuple) 
lblMessage.pack(fill=X)
lblBudgetOM = Label(zoneBtn, text="Budget OM")
lblBudgetOM.pack(fill=X)
lblBudgetOP = Label(zoneBtn, text="Budget OP")
lblBudgetOP.pack(fill=X)
btnArret = Button(zoneBtn, text="STOP", fg="yellow", bg="red", command=arret)
btnArret.pack(fill=X)
btnInit = Button(zoneBtn, text="START", fg="yellow", bg="green", command=depart)
btnInit.pack(fill=X)
# pour l'afficahge de mon record
lblBudgetRecord = Label(zoneBtn, text="Record : 0", fg="blue", bg="yellow", font=("calibri", 15))
lblBudgetRecord.pack(fill=X)


# creation du widget pour mon chronometre
lblDureePartie = Label(zoneBtn, text="Durée : 0s",fg="blue", bg="yellow",font=("calibri", 15))  # Affichage du temps
lblDureePartie.pack(fill=X)

# mise a jour du buget et du record 
afficher_budget_et_record()   # Met à jour l'affichage

#Rafraichissement de la fenêtre et de tout son contenu
fen_princ.mainloop()
