# -*- coding: utf-8 -*-
"""
Created on Tue May 27 14:36:39 2025

@author: NADAL NGAKI MUPATI
"""

#---Modules utilisés---

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#---création du visualiseur des fichiers CSV---
class VisualiseurCSV:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualiseur des données")
        self.root.geometry("600x550")
        texte_accueil=("Bienvenue dans le visualiseur des données\n\n"
                       "1. importez votre fichier csv en le chargeant dans l'endroit approprié\n"
                       "2. choisissez l'axe x et y selon selon l'entete de chaque colonne de votre fichier\n"
                       "3. appuyer sur le bouton : tracer le graphique\n")
        label_info = tk.Label(self.root, text=texte_accueil, justify="left", font=("calibri", 12))
        label_info.pack(pady=10)

        self.df = None
        
        # widgets 
        self.btn_charger = tk.Button(root, text ="charger un fichier CSV", command=self.charger_csv)
        self.btn_charger.pack(pady=10)
        
        self.colonne_x = ttk.Combobox(root, state='readonly')     # choix de l'axe en fonction de l'entete de la colonne
        self.colonne_y = ttk.Combobox(root, state='readonly')     # choix de l'axe en fonction de l'entete de la colonne
        
        self.btn_tracer = tk.Button(root, text="Tracer le graphique", command=self.tracer_graphique) 
        
        self.colonne_x.pack()
        self.colonne_y.pack()
        self.btn_tracer.pack(pady=10)
        
        self.canvas = None
        
#---fonction permettant de charger le fichier---

    def charger_csv(self):
        chemin = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")]) # permet le chargement des fichiers 
        if chemin:
            try:
                self.df = pd.read_csv(chemin)
                colonnes = list(self.df.columns)
                self.colonne_x['values'] = colonnes
                self.colonne_y['values'] = colonnes
                messagebox.showinfo("Succès", "Fichier téléchargé avec succès !")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lire le fichier : {e}")
                
#---fonction qui permet de réalier le gaphique---

    def tracer_graphique(self):
        if self.df is None :
            messagebox.showwarning("Attention", "Aucun fichier chargé.")
            return
        x_col = self.colonne.get()
        y_col = self.colonne.get()
        
        if x_col =="" or y_col =="":
            messagebox.showwarning("Attention", "choisis les colonnes X et Y." )
            return
        
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(self.df[x_col], self.df[y_col], marker='o')
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"{y_col} en fonction de {x_col}")
        ax.grid(True)
        
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = VisualiseurCSV(root)
    root.mainloop()

                                      