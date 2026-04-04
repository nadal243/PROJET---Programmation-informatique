# Documentation Technique - SurveillanceVideo.py

## Vue d'ensemble

Le script `SurveillanceVideo.py` est une application de vidéosurveillance intelligente développée en Python. Il capture la vidéo en temps réel à partir d'une webcam, détecte les mouvements et enregistre automatiquement les vidéos lorsqu'un mouvement est détecté.

**Auteur:** NGAKI MUPATI NADAL  
**Date de création:** 9 juin 2025  
**Version:** 1.0

---

## Fonctionnalités principales

1. **Capture vidéo en temps réel** - Récupération des images à partir de la webcam par défaut
2. **Détection de mouvement** - Algorithme basé sur la comparaison de frames successives
3. **Enregistrement automatique** - Enregistrement lancé lors de la détection de mouvement
4. **Interface graphique Tkinter** - Interface conviviale avec contrôles simples
5. **Alerte sonore** - Notification audio lors de la détection de mouvement

---

## Dépendances

```python
tkinter          # Interface graphique (généralement inclus avec Python)
cv2 (OpenCV)     # Capture vidéo et traitement d'image
PIL              # Conversion et affichage d'images
playsound        # Lecture de fichiers audio pour les alertes
```

### Installation des dépendances
```bash
pip install opencv-python pillow playsound
```

---

## Architecture

### Classe principale : `SurveillanceApp`

#### Initialisation (`__init__`)
Initialise l'interface graphique et les variables de contrôle.

**Variables d'instance:**
- `video_capture`: Objet de capture vidéo OpenCV
- `running`: État de la caméra (booléen)
- `previous_frame`: Image précédente en niveaux de gris (pour comparaison)
- `video_writer`: Objet d'écriture vidéo
- `recording`: État de l'enregistrement (booléen)
- `last_motion_time`: Timestamp du dernier mouvement détecté

**Composants d'interface:**
- `label_video`: Étiquette pour afficher la vidéo
- `btn_start`: Bouton de démarrage de la caméra
- `btn_stop`: Bouton d'arrêt de la caméra
- `btn_quit`: Bouton de fermeture de l'application

---

### Méthodes principales

#### 1. `start_camera()`
Lance la capture vidéo à partir de la webcam par défaut.

```python
# Active la vidéocapture (0 = webcam par défaut)
self.video_capture = cv2.VideoCapture(0)
```

**Actions:**
- Initialise l'objet `VideoCapture`
- Active le drapeau `running`
- Désactive le bouton "Démarrer"
- Active le bouton "Arrêter"
- Lance la boucle de mise à jour

---

#### 2. `MiseAJour_cadre()`
Boucle principale appelée tous les 10 ms pour traiter les frames en temps réel.

**Processus:**
1. Capture une frame depuis la vidéo
2. Convertit l'image en niveaux de gris
3. Applique un flou Gaussien (21x21) pour réduire le bruit
4. Compare avec la frame précédente
5. Détecte les mouvements si le nombre de pixels changeant > 5000
6. Lance l'enregistrement si un mouvement est détecté
7. Affiche l'image dans l'interface

**Paramètres de détection:**
- **Seuil de différence:** 25 (valeur pour la binarisation)
- **Seuil de mouvement:** 5000 pixels (nécessaire pour considérer un mouvement réel)
- **Délai d'arrêt:** 5 secondes sans mouvement avant de terminer l'enregistrement

**Format d'enregistrement:**
- Codec: XVID
- Format: .avi
- FPS: 20

---

#### 3. `stop_camera()`
Arrête la capture vidéo et libère les ressources.

**Actions:**
- Désactive le drapeau `running`
- Réinitialise les boutons
- Libère l'objet `VideoCapture`
- Termine tout enregistrement en cours

---

#### 4. `quit_app()`
Ferme l'application de manière propre.

**Actions:**
- Appelle `stop_camera()`
- Détruit la fenêtre Tkinter

---

## Algorithme de détection de mouvement

### Étapes:

1. **Conversion en niveaux de gris**
   ```python
   frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   ```

2. **Application d'un flou Gaussien**
   ```python
   frame_gray = cv2.GaussianBlur(frame_gray, (21, 21), 0)
   ```
   *Réduit le bruit et les petites variations*

3. **Calcul de la différence absolue**
   ```python
   diff = cv2.absdiff(self.previous_frame, frame_gray)
   ```

4. **Binarisation**
   ```python
   _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
   ```
   *Crée une image binaire (noir/blanc) des différences*

5. **Comptage des pixels modifiés**
   ```python
   motion_level = cv2.countNonZero(thresh)
   ```

6. **Décision**
   - Si `motion_level > 5000`: Mouvement détecté
   - Sinon: Pas de mouvement

---

## Flux de l'application

```
┌─────────────────────────────┐
│ Démarrage de l'application  │
└──────────────┬──────────────┘
               │
        ┌──────▼─────────┐
        │ Interface GUI  │
        └──────┬─────────┘
               │
        ┌──────▼──────────────────┐
        │ Attente du bouton START  │
        └──────┬───────────────────┘
               │
        ┌──────▼──────────────────────┐
        │ Initialisation VideoCapture │
        └──────┬───────────────────────┘
               │
    ┌──────────▼──────────────┐
    │ Boucle MiseAJour_cadre  │
    │ (tous les 10 ms)        │
    └──────┬───────────────────┘
           │
    ┌──────▼──────────────────┐
    │ Capture frame           │
    │ ↓ Conversion grise      │
    │ ↓ Flou Gaussien        │
    │ ↓ Comparaison          │
    └──────┬───────────────────┘
           │
    ┌──────▼──────────────────┐
    │ Détection mouvement ?   │
    └──────┬────────┬──────────┘
           │        │
        OUI│        │NON
           │        │
    ┌──────▼──┐  ┌──▼──────────────┐
    │Enregist-│  │Affichage vidéo  │
    │rement   │  │Vérif 5sec timeout│
    └─────────┘  └────────────���────┘
           │           │
           └──────┬────┘
                  │
           ┌──────▼──────────────┐
           │ Bouton STOP pressé? │
           └──────┬────┬──────────┘
                OUI│    │NON
                   │    │
              ┌────▼─┐ │
              │STOP  │ │
              └──────┘ │
                   ┌───▼────────┐
                   │Continuer   │
                   └────────────┘
```

---

## Guide d'utilisation

### Démarrage
```bash
python SurveillanceVideo.py
```

### Actions utilisateur
1. **Démarrer**: Cliquez sur "Démarrer" pour lancer la capture vidéo
2. **Arrêter**: Cliquez sur "Arrêter" pour arrêter la capture
3. **Quitter**: Cliquez sur "Quitter" pour fermer l'application

### Fichiers générés
- `mouvement.avi`: Vidéo enregistrée lors de la détection de mouvement
- `alerte.mp3`: Fichier audio pour l'alerte sonore (doit être présent dans le répertoire)

---

## Paramètres ajustables

| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| Taille du flou | (21, 21) | Noyau Gaussien - Augmenter pour plus de lissage |
| Seuil de binarisation | 25 | Sensibilité de la détection (0-255) |
| Seuil de mouvement | 5000 | Pixels minimum pour déclarer un mouvement |
| Délai d'arrêt | 5 secondes | Temps sans mouvement avant arrêt enregistrement |
| FPS enregistrement | 20 | Nombre d'images par seconde |
| Rafraîchissement GUI | 10 ms | Fréquence de mise à jour de l'affichage |

---

## Points à améliorer / Limitations

1. **Chemin dur du fichier audio**: `alerte.mp3` doit être dans le répertoire courant
2. **Chemin dur de la vidéo**: `mouvement.avi` est créé dans le répertoire courant
3. **Face recognition désactivée**: Importation commentée (ligne 6)
4. **Pas de configuration**: Les seuils sont en dur dans le code
5. **Gestion d'erreur limitée**: Pas de try/except pour les opérations critiques

---

## Recommandations

1. **Créer un fichier de configuration** pour les paramètres
2. **Ajouter la gestion des exceptions**
3. **Implémenter des options de sauvegarde** personnalisables
4. **Ajouter un logger** pour tracer les événements
5. **Tester différentes résolutions** selon votre webcam
6. **Activer face_recognition** si besoin de reconnaissance faciale

---

## Notes techniques

- **Conversion d'image**: PIL/Pillow est utilisé comme pont entre OpenCV (BGR) et Tkinter
- **Boucle d'événement**: Tkinter utilise `after()` pour faire fonctionner la détection en parallèle
- **VideoWriter**: Utilise le codec XVID pour la compression vidéo
- **Niveaux de gris**: Réduit la complexité de calcul par rapport aux images couleur

---

## Dépannage

| Problème | Cause | Solution |
|----------|-------|----------|
| Webcam ne s'ouvre pas | Index caméra incorrect | Vérifier que la caméra est connectée ou changer l'index |
| L'alerte sonore ne joue pas | Fichier `alerte.mp3` absent | Placer `alerte.mp3` dans le répertoire courant |
| Enregistrement ne démarre pas | Seuil de mouvement trop haut | Réduire la valeur `motion_level > 5000` |
| Application lente | Configuration système faible | Réduire la résolution ou augmenter l'intervalle `after()` |
| Erreur PIL/ImageTk | Image couleur BGR non convertie | Vérifier la conversion BGR→RGB |

---

**Dernière mise à jour:** 14 mars 2026
