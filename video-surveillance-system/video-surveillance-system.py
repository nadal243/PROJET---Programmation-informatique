"""
Created on Mon Jun  9 12:30:45 2025
@author: NGAKI MUPATI NADAL
"""

import tkinter as tk  # Pour créer l'interface graphique
import cv2  # OpenCV pour la capture vidéo et le traitement d'image
# import face_recognition  # (Désactivé ici, pas utilisé dans cette version)
from PIL import Image, ImageTk  # Pour afficher les images OpenCV dans Tkinter
from tkinter import messagebox  # Pour afficher des messages pop-up
import time  # Pour mesurer le temps écoulé (utile pour l'enregistrement)
from playsound import playsound  # Pour jouer un fichier audio (alerte sonore)


class SurveillanceApp:
    def __init__(self, root):
        self.root = root  
        self.root.title("Système de vidéosurveillance intelligent") 
        self.root.geometry("800x600") 

        # Initialisation des variables de contrôle
        self.video_capture = None         # Objet pour capturer la vidéo (webcam)
        self.running = False              # Indique si la caméra tourne
        self.previous_frame = None        # Image précédente en niveaux de gris (pour comparaison)
        self.video_writer = None          # Objet pour écrire les vidéos sur le disque
        self.recording = False            # Indique si un enregistrement est en cours
        self.last_motion_time = None      # Mémorise le moment du dernier mouvement

        # Interface graphique avec Tkinter
        self.label_video = tk.Label(self.root)  # Étiquette pour afficher la vidéo
        self.label_video.pack(pady=10)

        # Bouton pour démarrer la caméra
        self.btn_start = tk.Button(self.root, text="Démarrer", command=self.start_camera)
        self.btn_start.pack(side=tk.LEFT, padx=20)

        # Bouton pour arrêter la caméra
        self.btn_stop = tk.Button(self.root, text="Arrêter", command=self.stop_camera, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=20)

        # Bouton pour quitter l'application
        self.btn_quit = tk.Button(self.root, text="Quitter", command=self.quit_app)
        self.btn_quit.pack(side=tk.RIGHT, padx=20)

    def start_camera(self):
        # Ouvre la webcam (0 = webcam par défaut du PC)
        self.video_capture = cv2.VideoCapture(0)
        self.running = True  # Active la boucle de mise à jour
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.MiseAJour_cadre()  # Commence à lire les images

    def MiseAJour_cadre(self):
        # Fonction appelée en boucle pour afficher la vidéo et détecter les mouvements
        if self.running:
            ret, frame = self.video_capture.read()  # Capture une image
            if ret:
                # Convertit l'image couleur en niveaux de gris
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Applique un flou pour réduire les petits mouvements (bruit)
                frame_gray = cv2.GaussianBlur(frame_gray, (21, 21), 0)

                if self.previous_frame is None:
                    # Première image, on la garde pour comparer plus tard
                    self.previous_frame = frame_gray
                else:
                    # Compare l'image actuelle avec la précédente
                    diff = cv2.absdiff(self.previous_frame, frame_gray)
                    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)  # Binarise la différence
                    motion_level = cv2.countNonZero(thresh)  # Compte les pixels blancs (changements)

                    if motion_level > 5000:  # Si beaucoup de pixels ont changé → mouvement détecté
                        self.last_motion_time = time.time()  # On enregistre le moment du mouvement

                        if not self.recording:
                            # Si on ne filmait pas encore → démarrer un nouvel enregistrement
                            fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Format de vidéo .avi
                            self.video_writer = cv2.VideoWriter("mouvement.avi", fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                            self.recording = True  # Indique qu'on est en train d'enregistrer
                            messagebox.showinfo("Détection", "Mouvement détecté - enregistrement lancé")

                            # Alerte sonore
                            playsound("alerte.mp3", block=False)

                        # Enregistrement actif : on ajoute chaque image capturée à la vidéo
                        if self.video_writer is not None:
                            self.video_writer.write(frame)

                    # Si 5 secondes sont passées sans mouvement → arrêter l'enregistrement
                    if self.recording and self.last_motion_time and (time.time() - self.last_motion_time > 5):
                        self.video_writer.release()  # Ferme le fichier vidéo
                        self.video_writer = None
                        self.recording = False
                        messagebox.showinfo("Info", "Enregistrement terminé")

                    # Sauvegarder la dernière image pour la prochaine comparaison
                    self.previous_frame = frame_gray

                # Affiche l'image actuelle dans l'interface graphique
                img = Image.fromarray(frame)  # Convertit OpenCV → Image PIL
                imgtk = ImageTk.PhotoImage(image=img)  # Convertit Image PIL → Tkinter
                self.label_video.imgtk = imgtk
                self.label_video.configure(image=imgtk)

            # Rappelle cette fonction après 10 ms (boucle d'actualisation)
            self.root.after(10, self.MiseAJour_cadre)

    def stop_camera(self):
        # Arrête la caméra et libère les ressources
        self.running = False
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        if self.video_capture:
            self.video_capture.release()
            self.label_video.config(image="")

        self.previous_frame = None  # Réinitialise l'image précédente

        # Si une vidéo était en cours → on la termine proprement
        if self.recording and self.video_writer:
            self.video_writer.release()
            self.video_writer = None
            self.recording = False

    def quit_app(self):
        # Ferme proprement l'application
        self.stop_camera()
        self.root.destroy()


# Lancement de l'application principale
if __name__ == "__main__":
    root = tk.Tk()
    app = SurveillanceApp(root)
    root.mainloop()
