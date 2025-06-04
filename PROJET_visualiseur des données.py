# -*- coding: utf-8 -*-
"""
Created on Fri May 30 15:24:08 2025

@author: NADAL NGAKI MUPATI
"""

# Importation des bibliothèques nécessaires pour l'interface graphique, le traitement de données et la visualisation
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os 

class VisualiseurCSV:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualiseur des données CSV")
        self.root.geometry("1000x750")

        self.df = None
        self.canvas = None
        
        # Créer deux frames pour séparer les contrôles (gauche) et le graphique (droite)
        # Zone de gauche : contient les boutons et menus
        self.frame_gauche = tk.Frame(self.root)
        # Zone de droite : affichera le graphique
        self.frame_droite = tk.Frame(self.root)
        # Zone de gauche : contient les boutons et menus
        self.frame_gauche.pack(side=tk.LEFT, padx=20, pady=20, anchor='n')
        # Zone de droite : affichera le graphique
        self.frame_droite.pack(side=tk.LEFT, padx=20, pady=20, anchor='n')

        # -------- Interface utilisateur : affichage d'instructions --------
        label_info = tk.Label(
            self.frame_gauche,
            text="Bienvenue dans le visualiseur de données\n\n"
                 "1. Importez un fichier CSV ou Excel\n"
                 "2. Choisissez les colonnes X et Y\n"
                 "3. Choisissez le type de graphique\n"
                 "4. Cliquez sur 'Tracer le graphique'",
            justify="left",
            font=("Calibri", 12)
        )
        label_info.pack(pady=10)
        
        

        # Bouton pour charger un fichier CSV
        self.btn_charger = tk.Button(self.frame_gauche, text="Charger un fichier", command=self.charger_csv)
        self.btn_charger.pack(pady=10)

        # Combobox pour sélectionner les colonnes X et Y à partir des données
        self.colonne_x = ttk.Combobox(self.frame_gauche, state='readonly')
        self.colonne_y = ttk.Combobox(self.frame_gauche, state='readonly')
        self.colonne_x.pack(pady=5)
        self.colonne_y.pack(pady=5)
        
        # Sélection du type de graphique
        label_info = tk.Label(self.frame_gauche, text="selectionnez le type de graphique:", font=("calibri", 12))
        label_info.pack(pady=5)
        
        self.type_graphique = ttk.Combobox(self.frame_gauche, state='readonly')
        self.type_graphique['values'] = ['Ligne', 'Nuage de points', 'Barres', 'Histogramme']
        self.type_graphique.current(0)
        self.type_graphique.pack(pady=5)

        # Bouton pour tracer le graphique
        self.btn_tracer = tk.Button(self.frame_gauche, text="Tracer le graphique", command=self.tracer_graphique)
        self.btn_tracer.pack(pady=10)
        
        # Boutons de zoom
        self.btn_zoom_in = tk.Button(self.frame_gauche, text="Zoomer", command=self.zoom_in)
        self.btn_zoom_out = tk.Button(self.frame_gauche, text="Dézoomer", command=self.zoom_out)
        self.btn_reset_zoom = tk.Button(self.frame_gauche, text="Réinitialiser le zoom", command=self.reset_zoom)
        
        self.btn_zoom_in.pack(pady=5)
        self.btn_zoom_out.pack(pady=5)
        self.btn_reset_zoom.pack(pady=5)
        
        # Bouton pour sauvegarder le graphique
        self.btn_sauvegarder = tk.Button(self.frame_gauche, text="sauvegarder le graphique", command=self.SauvegaderGraphique)
        self.btn_sauvegarder.pack(pady=5)
        
        # Bouton pour supprimer le graphique
        self.btn_supprimer = tk.Button(self.frame_gauche, text="supprimer le graphique", command=self.supprimer_graphique)
        self.btn_supprimer.pack(pady=5)

    def charger_csv(self):
        # -------- Chargement du fichier CSV et extraction des colonnes --------
        chemin = filedialog.askopenfilename(
            filetypes=[
                ("Fichiers CSV et Excel", "*.csv *.xls *.xlsx"),
                ("Fichiers CSV", "*.csv"),
                ("Fichiers Excel", "*.xls *.xlsx")])
        if chemin:
            try:
                ext = os.path.splitext(chemin)[1].lower()
                if ext == ".csv":
                    self.df = pd.read_csv(chemin)
                elif ext in [".xls", ".xlsx"]:
                    self.df = pd.read_excel(chemin)
                else:
                    messagebox.showerror("Erreur, Format de fichier non pris en charge.")
                colonnes = list(self.df.columns)
                self.colonne_x['values'] = colonnes
                self.colonne_y['values'] = colonnes
                messagebox.showinfo("Succès", "Fichier chargé avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lire le fichier :\n{e}")

    def tracer_graphique(self):
        # -------- Vérification des conditions minimales --------
        if self.df is None:
            messagebox.showwarning("Attention", "Aucun fichier chargé.")
            return

        x_col = self.colonne_x.get()
        y_col = self.colonne_y.get()
        type_graph = self.type_graphique.get()

        if not x_col or not y_col:
            messagebox.showwarning("Attention", "Veuillez sélectionner les colonnes X et Y.")
            return

        try:
            # -------- Nettoyage des données : conversion en numérique et suppression des valeurs manquantes --------
            self.df[x_col] = pd.to_numeric(self.df[x_col], errors='coerce')
            self.df[y_col] = pd.to_numeric(self.df[y_col], errors='coerce')
            self.df.dropna(subset=[x_col, y_col], inplace=True)

            fig, ax = plt.subplots(figsize=(6, 4))
            self.ax = ax 

            # -------- Tracé du graphique selon le type sélectionné --------
            if type_graph == 'Ligne':
                ax.plot(self.df[x_col], self.df[y_col], marker='o')  # Graphique en ligne
            elif type_graph == 'Nuage de points':
                ax.scatter(self.df[x_col], self.df[y_col])           # Nuage de points
            elif type_graph == 'Barres':
                ax.bar(self.df[x_col], self.df[y_col])              # Diagramme en barres
            elif type_graph == 'Histogramme':
                ax.hist(self.df[y_col], bins=20, edgecolor='black') # Histogramme simple
                ax.set_xlabel(y_col)
                ax.set_ylabel("Fréquence")
                ax.set_title(f"Histogramme de {y_col}")
                ax.grid(True)
            else:
                messagebox.showwarning("Erreur", "Type de graphique non reconnu.")
                return

            # -------- Paramétrage général pour les autres types --------
            if type_graph != 'Histogramme':
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)
                ax.set_title(f"{y_col} en fonction de {x_col}")
                ax.grid(True)

            # Suppression de l'ancien graphique si présent
            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            # Affichage du graphique dans l’interface Tkinter
            self.canvas = FigureCanvasTkAgg(fig, master=self.frame_droite)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(pady=10)
            
            # FORCER le rendu puis sauvegarder les limites d'origine
            fig.canvas.draw()  # Très important
            self.original_xlim = self.ax.get_xlim()
            self.original_ylim = self.ax.get_ylim()
            
            # -------- Sauvegarde temporaire de la figure pour la fonction de sauvegarde --------
            self.current_fig = fig

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du tracé :\n{e}")
                
    def SauvegaderGraphique(self):
        # -------- Sauvegarde du graphique affiché en tant qu’image PNG --------
        if hasattr(self, 'current_fig'):
            fichier = filedialog.asksaveasfilename(defaultextension='.png',
                                                   filetypes=[("Fichier PNG", "*.png")])
            if fichier:
                try:
                    self.current_fig.savefig(fichier)
                    messagebox.showinfo("Succès", "Graphique sauvegardé avec succès.")
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible de sauvegarder le graphique :\n{e}")
        else:
            messagebox.showwarning("Avertissement", "Aucun graphique à sauvegarder.")
            
    def zoom_in(self):
        if self.ax:
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()
            self.ax.set_xlim([xlim[0] + (xlim[1] - xlim[0]) * 0.1, xlim[1] - (xlim[1] - xlim[0]) * 0.1])
            self.ax.set_ylim([ylim[0] + (ylim[1] - ylim[0]) * 0.1, ylim[1] - (ylim[1] - ylim[0]) * 0.1])
            self.canvas.draw()

    def zoom_out(self):
        if self.ax:
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()
            self.ax.set_xlim([xlim[0] - (xlim[1] - xlim[0]) * 0.1, xlim[1] + (xlim[1] - xlim[0]) * 0.1])
            self.ax.set_ylim([ylim[0] - (ylim[1] - ylim[0]) * 0.1, ylim[1] + (ylim[1] - ylim[0]) * 0.1])
            self.canvas.draw()
    
    def reset_zoom(self):
        if self.ax:
            if hasattr(self, 'original_xlim') and hasattr(self, 'original_ylim'):
                self.ax.set_xlim(self.original_xlim)
                self.ax.set_ylim(self.original_ylim)
            else:
                self.ax.relim()
                self.ax.autoscale_view()
            self.canvas.draw()
    
    def supprimer_graphique(self):
    #-----------permet d'effacer le graphique--------
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
            self.ax = None
            if hasattr(self, 'original_xlim'):
                del self.original_xlim
            if hasattr(self, 'original_ylim'):
                del self.original_ylim

# -------- Lancement de l'application --------
if __name__ == "__main__":
    root = tk.Tk()
    app = VisualiseurCSV(root)
    root.mainloop()
