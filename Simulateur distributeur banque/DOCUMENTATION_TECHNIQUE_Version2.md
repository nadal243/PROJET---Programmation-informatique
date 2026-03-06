
# Documentation Technique - Simulateur de Distributeur Bancaire

## 📋 Informations Générales

**Projet** : Simulateur de Distributeur Bancaire (DAB)  
**Auteur** : NADAL NGAKI MUPATI  
**Date de création** : 10 mai 2025  
**Langage** : Python 3  
**Dépendances** : tkinter (interface graphique)

---

## Description du Projet

Ce projet implémente un simulateur de distributeur bancaire avec une interface graphique basée sur tkinter. Il permet de gérer des comptes bancaires, effectuer des opérations courantes (dépôt, retrait, transfert) et consulter les soldes.

---

##  Architecture Générale

### Structure du Code

```
├── Fonctions de gestion des fichiers
│   ├── lire_compte()
│   └── ecrire_compte()
├── Fonctions métier
│   ├── creer_compte()
│   ├── voir_solde()
│   ├── faire_un_depot()
│   ├── faire_un_retrait()
│   └── faire_un_transfert()
└── Interface graphique principale
    └── Fenêtre Tkinter (root)
```

---

## 📁 Stockage des Données

### Fichier de Persistence

**Nom** : `compte.txt`  
**Format** : Texte simple (CSV)  
**Structure** : Une ligne par compte avec le format `nom,solde`

**Exemple** :
```
Alice,1500.50
Bob,2000.00
Charlie,500.75
```

### Initialisation

- Le fichier est créé automatiquement lors du premier dépôt/création de compte
- S'il n'existe pas, la fonction `lire_compte()` retourne une liste vide

---

##  Fonctions Principales

### 1. **Fonctions de Lecture/Écriture**

#### `lire_compte()`
```python
def lire_compte():
    """
    Lit tous les comptes depuis le fichier compte.txt
    
    Returns:
        list: Liste de tuples (nom, solde)
    
    Exception:
        - FileNotFoundError: Retourne une liste vide si le fichier n'existe pas
    """
```

**Logique** :
- Ouvre le fichier en mode lecture
- Parse chaque ligne au format "nom,solde"
- Convertit le solde en float
- Gère l'absence du fichier gracieusement

#### `ecrire_compte(comptes)`
```python
def ecrire_compte(comptes):
    """
    Écrit la liste des comptes dans le fichier compte.txt
    
    Args:
        comptes (list): Liste de tuples (nom, solde)
    """
```

**Logique** :
- Ouvre le fichier en mode écriture (remplace le contenu)
- Écrit chaque compte au format "nom,solde\n"

---

### 2. **Créer un Compte**

#### `creer_compte()`

**Fonctionnalités** :
- Ouvre une fenêtre secondaire (Toplevel)
- Demande le nom de l'utilisateur
- Validation du nom (non vide)
- Vérification de l'existence du compte
- Crée un nouveau compte avec solde initial = 0 €

**Fenêtre Secondaire** :
- Titre : "Création d'un compte"
- Dimensions : 400x200 pixels
- Champs : Entrée de texte pour le nom
- Bouton : "Valider"

**Messages de feedback** :
- ❌ "Nom invalide." (si vide)
- ❌ "Ce nom a déjà un compte." (si doublon)
- ✅ "Compte créé pour {nom} avec un solde de 0 €." (succès)

---

### 3. **Consulter le Solde**

#### `voir_solde()`

**Fonctionnalités** :
- Ouvre une fenêtre secondaire
- Demande le nom de l'utilisateur
- Recherche le compte dans la base
- Affiche le solde ou message d'erreur

**Fenêtre Secondaire** :
- Titre : "Vérification de solde"
- Dimensions : 400x200 pixels

**Messages de feedback** :
- 💰 "Solde de {nom} : {solde} €" (succès)
- ❌ "Compte introuvable." (erreur)

---

### 4. **Faire un Dépôt**

#### `faire_un_depot()`

**Fonctionnalités** :
- Ouvre une fenêtre secondaire
- Demande le nom et le montant
- Valide le montant (format numérique)
- Ajoute le montant au solde existant
- Persiste les modifications

**Fenêtre Secondaire** :
- Titre : "Faire un dépôt"
- Dimensions : 400x200 pixels
- Champs : Nom et montant

**Messages de feedback** :
- ✅ "{montant} € déposés. Nouveau solde : {nouveau_solde} €" (succès)
- ❌ "Montant invalide." (si non numérique)
- ❌ "Compte introuvable." (si le compte n'existe pas)

---

### 5. **Faire un Retrait**

#### `faire_un_retrait()`

**Fonctionnalités** :
- Ouvre une fenêtre secondaire
- Demande le nom et le montant
- Valide le montant
- Vérifie la suffisance des fonds
- Déduit le montant du solde

**Fenêtre Secondaire** :
- Titre : "Faire un retrait"
- Dimensions : 400x200 pixels

**Messages de feedback** :
- ✅ "{montant} € retirés. Nouveau solde : {nouveau_solde} €" (succès)
- ❌ "Montant invalide." (si non numérique)
- ❌ "Fonds insuffisants." (si solde < montant)
- ❌ "Compte introuvable." (si le compte n'existe pas)

---

### 6. **Faire un Transfert**

#### `faire_un_transfert()`

**Fonctionnalités** :
- Ouvre une fenêtre secondaire
- Demande l'expéditeur, destinataire et montant
- Valide le montant
- Vérifie l'existence des deux comptes
- Vérifie la suffisance des fonds chez l'expéditeur
- Débite l'expéditeur et crédite le destinataire

**Fenêtre Secondaire** :
- Titre : "Faire un transfert"
- Dimensions : 400x300 pixels
- Champs : Expéditeur, destinataire, montant

**Messages de feedback** :
- ✅ "Transfert de {montant} € de {expéditeur} à {destinataire} réussi." (succès)
- ❌ "Montant invalide." (si non numérique)
- ❌ "Compte expéditeur introuvable."
- ❌ "Compte destinataire introuvable."
- ❌ "Fonds insuffisants."

---

##  Interface Graphique Principale

### Configuration de la Fenêtre Principale

```python
root = tk.Tk()
root.title("BANQUE FRANCE-AFRIQUE")
root.geometry("700x650")
root.configure(bg="#DDEEFF")
```

**Caractéristiques** :
- Titre : "BANQUE FRANCE-AFRIQUE"
- Dimensions : 700x650 pixels
- Couleur de fond : Bleu ciel (#DDEEFF)

### Composants Principaux

#### 1. Label d'Accueil
- Texte de bienvenue avec liste des opérations
- Police : Calibri, taille 14
- Couleur : Rouge
- Largeur max : 600 pixels (wraplength)

#### 2. Label de Résultat
- Affiche les messages de feedback des opérations
- Police : Arial, taille 14
- Couleur : Bleu

#### 3. Frame de Boutons
- Conteneur pour les 6 boutons d'action
- Disposition : Grille (grid layout)
- Espacement : 5 pixels entre les boutons

#### 4. Boutons d'Action

| # | Texte | Fonction | Ligne |
|---|-------|----------|-------|
| 1 | Créer un compte | creer_compte() | 0 |
| 2 | Voir le solde | voir_solde() | 1 |
| 3 | Faire un dépôt | faire_un_depot() | 2 |
| 4 | Faire un retrait | faire_un_retrait() | 3 |
| 5 | Faire un transfert | faire_un_transfert() | 3 |
| 6 | Quitter | root.destroy() | 4 |

⚠️ **Remarque** : Les boutons 4 et 5 occupent la même ligne (row=3), ce qui peut créer un chevauchement visuel.

---

##  Bugs et Limitations Identifiés

### 1. **Chevauchement des boutons 4 et 5**
```python
btn_retrait = tk.Button(frame_boutons, text="4. Faire un retrait", width=30, command=faire_un_retrait)
btn_retrait.grid(row=3, column=0, pady=5)

btn_transfert = tk.Button(frame_boutons, text="5. Faire un transfert", width=30, command=faire_un_transfert)
btn_transfert.grid(row=3, column=0, pady=5)  # ❌ Même position !
```

**Solution** : Utiliser `row=4` pour le bouton transfert.

### 2. **Fermeture incohérente des fenêtres**
- `creer_compte()` : Ferme la fenêtre après la création
- `voir_solde()` : Ferme la fenêtre après affichage
- `faire_un_depot()` : Ferme la fenêtre après le dépôt
- `faire_un_retrait()` : Ne ferme PAS la fenêtre en cas de montant invalide (bug)
- `faire_un_transfert()` : Ferme toujours la fenêtre

**Solution** : Homogénéiser la gestion des fermetures.

### 3. **Pas de validation de montant négatif**
Les fonctions acceptent les montants négatifs :
```python
montant = float(entre_montant2.get())  # Accepte -500, -1000, etc.
```

**Solution** : Ajouter une vérification `if montant <= 0:`.

### 4. **Pas de gestion d'erreurs lors de la sauvegarde**
Si le disque est plein ou les permissions insuffisantes, `ecrire_compte()` planterra.

---

##  Flux de Données

### Création de Compte

```
Clic "Créer un compte"
    ↓
Fenêtre secondaire
    ↓
Utilisateur saisit le nom
    ↓
Clic "Valider"
    ↓
Validation nom (non vide ?)
    ↓
Lecture du fichier (lire_compte)
    ↓
Vérification doublon
    ↓
Ajout du compte (nom, 0.0)
    ↓
Écriture du fichier (ecrire_compte)
    ↓
Message de feedback
    ↓
Fermeture de la fenêtre
```

### Dépôt/Retrait

```
Clic "Faire un dépôt/retrait"
    ↓
Fenêtre secondaire
    ↓
Utilisateur saisit nom + montant
    ↓
Clic "Valider"
    ↓
Validation montant (numérique ?)
    ↓
Lecture du fichier (lire_compte)
    ↓
Recherche du compte
    ↓
Vérification (retrait : fonds suffisants ?)
    ↓
Mise à jour du solde
    ↓
Écriture du fichier (ecrire_compte)
    ↓
Message de feedback
    ↓
Fermeture de la fenêtre
```

---

## 🔒 Sécurité et Considérations

### Points Faibles

1. **Pas d'authentification** : N'importe qui peut accéder à n'importe quel compte
2. **Pas de chiffrement** : Les données sont en texte clair
3. **Pas d'historique** : Pas de trace des transactions
4. **Pas de concurrence** : Une seule instance peut utiliser l'app
5. **Noms non uniques au niveau système** : Pas de PIN/mot de passe

### Recommandations

- Ajouter un système d'authentification
- Implémenter un historique des transactions
- Chiffrer le fichier de données
- Ajouter des logs d'audit
- Gérer les permissions utilisateur

---

##  Conventions de Code

### Nommage
- **Variables** : snake_case (`entre_nom`, `montant_invalide`)
- **Fonctions** : snake_case (`lire_compte`, `faire_un_depot`)
- **Constantes** : UPPER_SNAKE_CASE (`FICHIER`)

### Formatage
- **Encodage** : UTF-8 (déclaré : `# -*- coding: utf-8 -*-`)
- **Indentation** : 4 espaces
- **Longueur de ligne** : Respectée (pas de dépassement)

### Documentation
- Manque de docstrings pour les fonctions
- Commentaires limités
- Pas de type hints

---

##  Améliorations Futures Suggérées

### Court Terme
1. ✅ Corriger le chevauchement des boutons 4 et 5
2. ✅ Ajouter la validation des montants négatifs
3. ✅ Homogénéiser la gestion des fenêtres secondaires
4. ✅ Ajouter des docstrings

### Moyen Terme
1. 🔐 Implémenter l'authentification (PIN/password)
2. 📊 Ajouter un historique des transactions
3. 🔍 Recherche et affichage de tous les comptes
4. 💾 Utiliser une base de données (SQLite) au lieu de fichiers texte

### Long Terme
1. 🛡️ Chiffrer les données sensibles
2. 🌐 Implémenter une API REST
3. 📱 Créer une interface mobile
4. 📈 Ajouter des graphiques (solde dans le temps)

---

## 📋 Checklist de Test

- [ ] Créer un compte avec un nom valide
- [ ] Tenter de créer deux comptes avec le même nom
- [ ] Consulter le solde d'un compte existant
- [ ] Consulter le solde d'un compte inexistant
- [ ] Déposer un montant positif
- [ ] Déposer un montant invalide (texte)
- [ ] Retirer un montant valide (solde suffisant)
- [ ] Retirer plus que le solde disponible
- [ ] Transférer de A à B (solde suffisant)
- [ ] Transférer vers un compte inexistant
- [ ] Vérifier la persistance des données (relancer le program)

---

##  Auteur et Maintenance

**Auteur Original** : NADAL NGAKI MUPATI  
**Date** : 10 mai 2025

Projet personnel 

Pour toute question ou contribution, veuillez contacter l'auteur.

---

**Fin de la Documentation Technique**
