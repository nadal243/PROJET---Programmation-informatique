# Documentation Technique - Jeu Vidéo Eco-Guerrier

## Table des Matières

1. [Vue d'ensemble du projet](#vue-densemble-du-projet)
2. [Architecture globale](#architecture-globale)
3. [Modules et fonctions](#modules-et-fonctions)
4. [Mécaniques de jeu](#mécaniques-de-jeu)
5. [Système d'IA](#système-dia)
6. [Structure des fichiers](#structure-des-fichiers)
7. [Installation et configuration](#installation-et-configuration)
8. [Guide d'utilisation](#guide-dutilisation)
9. [Spécifications techniques](#spécifications-techniques)
10. [Notes de développement](#notes-de-développement)

---

## Vue d'ensemble du projet

### Objectif
**"OCEAN WAR L1 SPI"** est un jeu de stratégie écologique en temps réel où deux organismes (OMI et OPEP) s'affrontent dans un environnement marin. Le joueur contrôle l'OMI (Organisation Maritime Internationale) pour combattre la pollution pétrolière et protéger les écosystèmes marins.

### Thématique
- **OMI (Maritime)** : Organisation de protection de l'environnement marin
- **OPEP (Pétrole)** : Organisation d'extraction pétrolière
- **Navires Pirates** : Entités autonomes qui attaquent les navires OPEP
- **Nappes Hydrocarbures** : Zones de pollution à nettoyer

### Technologies
- **Langage** : Python 3
- **Interface graphique** : Tkinter
- **Calculs numériques** : NumPy
- **Algorithme de navigation** : Algorithme de Lee (recherche de chemin)

---

## Architecture globale

### Flux d'exécution principal

```
┌─────────────────────────────────────┐
│   Initialisation (main)              │
│   - Fenêtre Tkinter                 │
│   - Canvas                          │
│   - Images et cartes                │
└──────────────┬──────────────────────┘
               │
        ┌──────▼──────┐
        │  depart()   │ (Appui START)
        │ Réinitialise│
        └──────┬──────┘
               │
        ┌──────▼──────────────────────┐
        │  gestion_deplacements()     │
        │  (Boucle principale)        │
        │  - Déplace les entités      │
        │  - Gère collisions          │
        │  - Mise à jour budgets      │
        │  - Vérifie victoire/défaite │
        └──────┬──────────────────────┘
               │
        ┌──────▼──────┐
        │   arret()   │ (Appui STOP)
        │ Fin de jeu  │
        └─────────────┘
```

### Structure des données principales

```python
# Entités mobiles (index alignés)
entitesMobiles[]           # IDs des images canvas
typesEntiteMobile[]        # Types (OMI, OPEP, NAPPE, PIRATE)
etats_chargement[]         # État 0-100 (vide à plein)

# Positions (coordonnées réelles)
coord_iEntitesMobiles[]    # Positions X actuelles
coord_jEntitesMobiles[]    # Positions Y actuelles
coord_iEntitesMobiles_Init[] # Positions X initiales
coord_jEntitesMobiles_Init[] # Positions Y initiales

# Vélocités
vitX[]                     # Vitesse X (pixels/update)
vitY[]                     # Vitesse Y (pixels/update)

# Carte
matValCarteN1[17x17]       # Matrice principale
matValCarteN1_initial      # Copie de sauvegarde
matImgCarteN1[17x17]       # IDs des images canvas

# Budget (économie du jeu)
budgetOM, budgetOP         # Budgets actuels
```

---

## Modules et fonctions

### 1. **AlgoLee_v02.py** - Algorithme de pathfinding

#### Fonction : `calculLaby()`
```python
def calculLaby(pLaby, pValsDisponibles, xDepart, yDepart, xArrivee, yArrivee)
```

**Objectif** : Calculer le chemin optimal entre deux points en utilisant l'algorithme de Lee

**Paramètres** :
- `pLaby` : Matrice du labyrinthe
- `pValsDisponibles` : Types de zones naviguables (ex: [10, 11])
- `xDepart, yDepart` : Coordonnées de départ
- `xArrivee, yArrivee` : Coordonnées d'arrivée

**Retour** : Direction à prendre `[dx, dy]`
- Haut : `[0, 1]`
- Bas : `[0, -1]`
- Gauche : `[-1, 0]`
- Droite : `[1, 0]`

**Algorithme** :
1. Initialiser une matrice distance avec valeur maximale
2. Marquer distance[départ] = 0
3. Parcourir tous les voisins (connexité 4) et étiqueter les distances
4. Rechercher le voisin de l'arrivée avec la distance minimale
5. Retourner la direction vers ce voisin

**Connexité** : 4-connectée (haut, bas, gauche, droite)

---

### 2. **ProjetL1Algo25_v02.py** - Moteur de jeu principal

#### Gestion de l'initialisation

##### `creationEntiteMobile(pTypeEntiteMobile)`
Crée une nouvelle entité mobile (navire, nappe, pirate)

**Types d'entités** :
- `TYPE_ORGA_MARITIME (1)` : Navire OMI - Au départ : `BM` (base maritime)
- `TYPE_ORGA_PETROL (5)` : Navire OPEP - Au départ : `BP` (base pétrolière)
- `TYPE_NAPPE_HYDRO (6)` : Nappe hydrocarbure - Au départ : `PP` (plateforme pétrolière)
- `NAVIRE_PIRATE (4)` : Navire pirate - Spawn aléatoire en `ZN`

#### Gestion des déplacements

##### `gestion_deplacements()`
**Boucle principale du jeu** (appelée toutes les 100ms)

Responsabilités :
- Mettre à jour les positions des entités
- Gérer les évolutions des zones (PP, ZP)
- Appeler la vérification victoire/défaite
- Programmer le prochain appel (récursion)

**Variables globales modifiées** :
- `dureePP`, `dureeZP` : Décompte des durées
- `dureeSimulation` : Temps total écoulé
- `coord_iEntitesMobiles`, `coord_jEntitesMobiles` : Nouvelles positions

##### `deplacement(pNoEntiteMobile)`
**Cœur de la physique du jeu** pour une entité

Étapes :
1. **Alignement** : Si changement d'axe, arrondir l'axe perpendiculaire
2. **Déplacement** : `coord += vitesse`
3. **Détection de cellule** : Utiliser `ceil()` ou `floor()` selon direction
4. **Vérifications** :
   - Collision avec terrain → Repositionner et arrêter
   - Collision avec zone protégée (ZP) + nappe → Dégât (-500 OMI)
   - Arrivée navire OMI à port (BM) chargé → Décharge (+100 OMI)
   - Arrivée navire OPEP à plateforme (PP) vide → Charge, créer nappe
   - Arrivée navire OPEP à port (BP) chargé → Décharge (+100 OPEP)
   - Collision entre entités → Appliquer logiques spéciales

5. **Mises à jour visuelles** : Redessiner l'entité

##### `chgtDirectionOP(pNoEntiteMobile)`
Gère l'IA autonome des entités non-joueur

**Comportements** :
- **Navire OPEP** : Navigation intelligente vers PP (si vide) ou BP (si chargé)
- **Navire Pirate** : Mouvement aléatoire avec changement occasionnel (2% par frame)

##### `pilotage(pNoEntiteMobile, pVitesseX, pVitesseY)`
Applique les commandes du joueur au navire OMI

**Contrôles** :
- Flèche Haut/Bas : Déplacement vertical
- Flèche Gauche/Droite : Déplacement horizontal
- Vitesse OMI : 0.04 pixels/update
- Vitesse OPEP : 0.03 pixels/update
- Vitesse Pirate : 0.06 pixels/update

---

#### Gestion des événements clavier

##### `evenements(event)`
Dispatcher les événements clavier

| Touche | Action |
|--------|--------|
| `↑/↓/←/→` | Déplacer le navire OMI |
| `Space` | Démarrer le jeu |
| `Escape` | Arrêter le jeu |
| `N` | Nettoyer une nappe hydrocarbure (si adjacente) |
| `V` | Ajouter une nouvelle zone protégée (ZP) |
| `P` | Déplacer la plateforme pétrolière (PP) |

---

#### Gestion de l'économie

##### `sauvegarder_budget(budget)`
Ajoute un nouveau score au fichier `budget.txt`

```python
fichier.write(f"{budget}\n")  # Nouvelle ligne par score
```

##### `charger_record()`
Charge le meilleur budget de tous les temps

##### `afficher_classement_final(budget_final)`
Affiche le classement final du joueur

---

#### Gestion des zones dynamiques

##### `ajout_de_nouvelles_zones_protegées()`
Crée une nouvelle zone protégée (ZP) sur une zone neutre (ZN)

- Recherche une zone `ZN` avec 8 voisins disponibles
- Change le type à `ZP`
- Met à jour l'image canvas

##### `deplacement_de_la_plateforme_petroliere()`
Déplace la plateforme pétrolière (PP) vers une nouvelle zone

---

#### Utilitaires

##### `getCoordAleatoire(pTypesZones, pVoisinsEgalement=False, pBordure=0)`
Tire une coordonnée aléatoire d'un type de zone spécifique

**Options** :
- `pVoisinsEgalement` : S'assurer que les 8 voisins sont du bon type
- `pBordure` : Nombre de cases de bordure à ignorer

##### `getCelluleZoneUnique(pTYPE_ZONE)`
Trouve l'unique cellule d'un type (ex: recherche de la plateforme PP)

##### `getCelluleEntiteMobile(pNoEntiteMobile)`
Convertit les coordonnées réelles d'une entité en indices matriciels

```python
return [round(coord_i), round(coord_j)]
```

##### `getConvertCoordNiveauEnCoordPixels(i, j)`
Conversion matriciel → pixel

```python
x = LARG_CASE * i      # 40 * i
y = HAUT_CASE * j      # 40 * j
```

##### `getConvertCoordPixelsEnCoordNiveau(x, y)`
Conversion pixel → matriciel

##### `voisinsDisponibles(pLaby, pValsDisponibles, pX, pY)`
Retourne les 8 voisins (ou moins) qui ont un type autorisé

**Connexité** : 8-connectée (include diagonales)

---

#### Gestion de l'affichage

##### `CreationImagesCarte()`
Crée ou recrée la grille de décor

- Supprime les anciennes images
- Réinitialise `matValCarteN1` depuis la sauvegarde
- Créée une image pour chaque cellule selon son type

##### `deplacerImage(im, newX, newY)`
Met à jour les coordonnées d'une image canvas

---

#### Gestion de l'état du jeu

##### `depart()`
**Initialisation complète du jeu**

Étapes :
1. Réinitialiser toutes les vitesses à 0
2. Réinitialiser les états de chargement
3. Restaurer les positions initiales
4. Recréer les images de la carte
5. Activer les animations
6. Démarrer la boucle `gestion_deplacements()`
7. Supprimer les nappes restantes du tour précédent

##### `arret()`
**Arrêt sans réinitialisation**

Définit `dde_arret = True` pour stopper la boucle

##### `VictoireDefaite()`
**Vérification des conditions de fin**

Victoire si :
- Plus aucune zone neutre avec 8 voisins libres (toutes protégées)
- `budgetOP < 0` (OPEP en faillite)

Défaite si :
- `budgetOM < 0` (OMI en faillite)

---

#### Gestion du chronomètre

##### `miseAJourDuree()`
Met à jour l'affichage du temps écoulé toutes les secondes

```python
if chrono_actif:
    duree_partie += 1
    lblDureePartie.config(text=f"Durée : {duree_partie}s")
    fen_princ.after(1000, miseAJourDuree)
```

---

#### Gestion des nappes hydrocarbures

##### `suppression_des_nappes_hydocarbures()`
Supprime une nappe hydrocarbure (touche N)

- Cherche une nappe au `ETAT_CHARGEMENT_MAX`
- Supprime l'image canvas
- Supprime toutes les données associées
- Ajoute une sanction à OPEP (-500)
- Ajoute un traitement à OMI (+100)

---

### 3. **budget.txt** - Base de données des scores

**Format** : Un budget par ligne, valeurs numériques

**Utilisation** :
- Chargé au démarrage pour afficher le record
- Mis à jour lors de chaque fin de partie
- Trié pour établir un classement

---

## Mécaniques de jeu

### Économie

| Action | Budget OMI | Budget OPEP |
|--------|-----------|-----------|
| Nettoyer nappe à port | +100 | — |
| Intercepter nappe | +100 | — |
| Nappe atteint zone protégée | -500 | — |
| Vendre pétrole | — | +100 |
| Nappe interceptée | — | -500 |
| Navire pirate attaque | — | -500 |

### États de chargement

```
ETAT_CHARGEMENT_MIN = 0   (Vide)
ETAT_CHARGEMENT_MAX = 100 (Plein)
```

**Transitions** :
- OMI vide : À la base (BM)
- OMI plein : À la plateforme (PP) ou en route
- OPEP vide : À la base (BP)
- OPEP plein : À la plateforme (PP) ou en route
- Nappe : Toujours pleine (100) jusqu'à suppression

---

## Système d'IA

### 1. **Navire OPEP** - IA Intelligente

```python
if etats_chargement == ETAT_CHARGEMENT_MAX:
    cible = getCelluleZoneUnique(BP)  # Port
else:
    cible = getCelluleZoneUnique(PP)  # Plateforme
```

**Logique de navigation** :
- Calculer la différence entre position et cible
- Se déplacer vers la plus grande différence (X puis Y)
- Monoaxial : déplacement sur un seul axe à la fois

### 2. **Navire Pirate** - IA Aléatoire

```
Probabilité 2% par frame : changer de direction
Sinon : continuer dans la même direction
```

**Directions possibles** :
- `(VIT_PIRATE, 0)` - Droite
- `(-VIT_PIRATE, 0)` - Gauche
- `(0, VIT_PIRATE)` - Bas
- `(0, -VIT_PIRATE)` - Haut

**Comportement** :
- Attaque tout navire OPEP chargé
- Supprime le chargement du navire OPEP

---

## Structure des fichiers

### Dossier `jeu vidéo_eco-guerrier/`

```
jeu vidéo_eco-guerrier/
├── ProjetL1Algo25_v02.py      # Moteur de jeu principal
├── AlgoLee_v02.py              # Algorithme de pathfinding
├── budget.txt                  # Base de données des scores
└── img/                         # Ressources graphiques
    ├── ocean40.gif             # Zone neutre (ZN)
    ├── protection40.gif        # Zone protégée (ZP)
    ├── terrainCC40.gif         # Terrain impassable (ZT)
    ├── port40red.gif           # Base OPEP (BP)
    ├── port40green.gif         # Base OMI (BM)
    ├── platform40.gif          # Plateforme pétrolière (PP)
    ├── bateauOMI40empty.gif    # Navire OMI vide
    ├── bateauOMI40full.gif     # Navire OMI chargé
    ├── bateauOPEP40empty.gif   # Navire OPEP vide
    ├── bateauOPEP40full.gif    # Navire OPEP chargé
    ├── hydrocarbure40a.gif     # Nappe hydrocarbure
    ├── ecoboat40.gif           # Navire pirate
    ├── terrainHG40.gif         # Coin haut-gauche (CG)
    ├── terrainHD40.gif         # Coin haut-droit (CD)
    ├── terrainBG40.gif         # Coin bas-gauche (CGh)
    ├── terrainBD40.gif         # Coin bas-droit (CDh)
    ├── terrainCH40.gif         # Côté haut (CH)
    ├── terrainCB40.gif         # Côté bas (CB)
    ├── terrainCG40.gif         # Coin gauche haut (cG)
    ├── terrainCD40.gif         # Coin droit haut (cD)
```

---

## Installation et configuration

### Prérequis

```
Python 3.7+
tkinter (inclus avec Python)
numpy
```

### Installation des dépendances

```bash
pip install numpy
```

### Structure de répertoires requise

```
ProjetL1Algo25_v02.py
img/
  └── [tous les fichiers .gif]
budget.txt (créé automatiquement)
```

### Lancement

```bash
python ProjetL1Algo25_v02.py
```

---

## Guide d'utilisation

### Démarrage du jeu

1. Lancer le script : `python ProjetL1Algo25_v02.py`
2. Cliquer sur le bouton **START** (vert)
3. Le chronomètre démarre

### Commandes de jeu

| Touche | Action |
|--------|--------|
| `↑` | Navire OMI vers le haut |
| `↓` | Navire OMI vers le bas |
| `←` | Navire OMI vers la gauche |
| `→` | Navire OMI vers la droite |
| `Space` | Redémarrer une partie |
| `Escape` | Arrêter la partie |
| `N` | Nettoyer une nappe (proximité requise) |
| `V` | Ajouter une zone protégée |
| `P` | Déplacer la plateforme pétrolière |

### Objectifs

**Victoire** : Réduire OPEP à la faillite (budget ≤ 0) OU protéger toutes les zones libres

**Défaite** : Votre budget (OMI) tombe à 0

### Interface

```
┌─────────────────────────────────┐
│ Navire OMI (joueur)    STOP ■    │
│                        START ■   │
│ Zone Protégée (défense)          │
│ Zone Neutre (à protéger)         │
│ Nappe Hydrocarbure (à nettoyer)  │
│                                 │
│ Navire OPEP (ennemi)            │
│ Navire Pirate (allié)           │
│ Plateforme Pétrolière (OPEP)   │
│ Port OMI (décharge)             │
│ Port OPEP (décharge)            │
└─────────────────────────────────┘
```

---

## Spécifications techniques

### Constantes du jeu

```python
# Vitesses (pixels/update @ 100ms)
VIT_MAX_OrgaMaritime = 0.04      # Lent mais contrôlé
VIT_MAX_OrgaPetrole = 0.03       # Très lent
VIT_MAX_NAVIRE_PIRATE = 0.06     # Rapide

# Économie
tarifSANCTION = 500              # Pénalité OPEP (nappe prise)
tarifVENTE = 100                 # Gain OPEP (pétrole déchargé)
tarifTRAITEMENT = 100            # Gain OMI (nappe nettoyée)
tarifDEGAT = 500                 # Perte OMI (zone protégée détruite)

# Budgets initiaux
budgetOM_INIT = 5000
budgetOP_INIT = 5000

# Durées d'exploitation (secondes)
dureePP_Initiale = 20            # Plateforme productive 20s
dureeZP_Initiale = 20            # Zone protégée 20s

# Affichage
LARG_CASE = 40                   # Pixel par cellule
HAUT_CASE = 40
LARG_CANVAS = 17 * 40 = 680      # 17x17 grille
HAUT_CANVAS = 17 * 40 = 680
tpsRafraichissement = 0.1        # 100ms par update
```

### Coordonnées et conversions

```python
# Matriciel [i][j] où :
# i = colonne (0-16, gauche à droite)
# j = ligne (0-16, haut en bas)

# Pixel (X, Y) :
# X = i * 40 (horizontal)
# Y = j * 40 (vertical)

# Conversion :
# matriciel → pixel : (i*40, j*40)
# pixel → matriciel : (int(x/40), int(y/40))
```

### Types de zones (valeurs matricielles)

```python
ZN = 10    # Zone neutre
ZP = 11    # Zone protégée
BP = 20    # Base OPEP
PP = 30    # Plateforme pétrolière
BM = 40    # Base OMI
ZT = 50    # Terrain impassable
CG, CD, CDh, CGh, CH, CB, cG, cD  # Bordures
```

### Types d'entités

```python
TYPE_ORGA_MARITIME = 1    # Navire OMI
TYPE_ORGA_PETROL = 5      # Navire OPEP
TYPE_NAPPE_HYDRO = 6      # Nappe hydrocarbure
NAVIRE_PIRATE = 4         # Navire pirate
```

---

## Notes de développement

### Versions et historique

**v2.0** :
- Bug Restart : Suppression des nappes hydrocarbures résiduelles
- Bug Navigation OPEP : Correction de l'IA

**v2.1** :
- Ajout du système de chronomètre
- Historique des budgets dans `budget.txt`
- Affichage du record personnel

**v2.2** :
- Navigation OPEP optimisée
- Navires pirates ajoutés (5 instances)
- Système d'attaque pirate implémenté

### Bugs connus

1. **Coordonnées matricielles inversées** : `pLaby[Y][X]` vs `[X][Y]`
   - Voir le code de `deplacement()` et `AlgoLee_v02.py`
   - Convention : la matrice utilise `[j][i]` (ligne, colonne)

2. **Alignement des axes** : Les navires s'alignent avant de changer d'axe
   - Peut causer des mouvements non-fluides avec changements rapides

3. **Collision Z-order** : Les nappes peuvent passer sous les navires visuellement

### Optimisations futures

1. **Pathfinding** : Implémenter A* au lieu de l'algorithme de Lee
2. **Multithreading** : Déplacer les calculs IA dans des threads séparés
3. **Ressources graphiques** : Utiliser PNG ou sprites animés
4. **Persistance** : Base de données SQLite au lieu de TXT
5. **Réseau** : Mode multijoueur (joueur vs joueur)
6. **Son** : Effets sonores et musique de fond

### Points d'entrée d'extension

1. **Nouveaux types d'entités** : Ajouter un `TYPE_X` et gérer dans `creationEntiteMobile()`
2. **Nouveaux types de zones** : Ajouter une constante et une image dans `CreationImagesCarte()`
3. **Nouvelles mécaniques** : Modifier `deplacement()` pour ajouter des interactions
4. **Nouvelles IA** : Implémenter une fonction `comportement_X()` et l'appeler dans `chgtDirectionOP()`

---

## Contact et support

**Auteur** : NGAKI MUPATI NADAL  
**Sujet** : L1 SPI - Sujet 11 (Eco Guerrier)  
**Repository** : https://github.com/nadal243/PROJET---Programmation-informatique
