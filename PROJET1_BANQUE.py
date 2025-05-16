# -*- coding: utf-8 -*-
"""
Created on Sat May 10 12:55:53 2025

@author: NADAL NGAKI MUPATI
"""

import tkinter as tk

FICHIER = "compte.txt"

# --- Fonctions de lecture/écriture du fichier ---

def lire_compte():
    comptes = []
    try:
        with open(FICHIER, 'r') as f:
            for ligne in f:
                ligne = ligne.strip()
                if ligne:
                    nom, solde = ligne.split(',')
                    comptes.append((nom, float(solde)))
    except FileNotFoundError:
        pass
    return comptes

def ecrire_compte(comptes):
    with open(FICHIER, 'w') as f:
        for nom, solde in comptes:
            f.write(f"{nom},{solde}\n")

# --- Création d'un compte avec fenêtre secondaire ---

def creer_compte():
    def valider_creation():
        nom = entre_nom.get().strip()
        if not nom:
            label_result.config(text="❌ Nom invalide.")
            return

        comptes = lire_compte()
        for n, _ in comptes:
            if n == nom:
                label_result.config(text="❌ Ce nom a déjà un compte.")
                fenetre_creation.destroy()
                return

        comptes.append((nom, 0.0))
        ecrire_compte(comptes)
        label_result.config(text=f"✅ Compte créé pour {nom} avec un solde de 0 €.")
        fenetre_creation.destroy()

    # Fenêtre secondaire
    fenetre_creation = tk.Toplevel(root)
    fenetre_creation.title("Création d'un compte")
    fenetre_creation.geometry("400x200")

    label_info = tk.Label(fenetre_creation, text="Saisir votre nom d'utilisateur :", font=("Arial", 12))
    label_info.pack(pady=10)

    entre_nom = tk.Entry(fenetre_creation, width=30)
    entre_nom.pack(pady=5)

    bouton_valider = tk.Button(fenetre_creation, text="Valider", command=valider_creation)
    bouton_valider.pack(pady=10)

# --- Voir le solde ---

def voir_solde():
    def valider_solde():
        nom = entre_nom1.get().strip()
        comptes = lire_compte()
    
        for n, solde in comptes:
            if n == nom:
                label_result.config(text=f"💰 Solde de {nom} : {solde} €")
                fenetre_creation1.destroy()
                return
        label_result.config(text="❌ Compte introuvable.")
        fenetre_creation1.destroy()
        
        
    fenetre_creation1 = tk.Toplevel(root)
    fenetre_creation1.title("verification de solde")
    fenetre_creation1.geometry("400x200")

    label_info1 = tk.Label(fenetre_creation1, text="Saisir votre nom d'utilisateur :", font=("Arial", 12))
    label_info1.pack(pady=10)

    entre_nom1 = tk.Entry(fenetre_creation1, width=30)
    entre_nom1.pack(pady=5)
    
    bouton_valider1 = tk.Button(fenetre_creation1, text="Valider", command=valider_solde)
    bouton_valider1.pack(pady=10)

# --- Dépôt d'argent ---

def faire_un_depot():
    def valider_depot():
        
        nom = entre_nom2.get().strip()
        try:
            montant = float(entre_montant2.get())
        except ValueError:
            label_result.config(text="❌ Montant invalide.")
            fenetre_creation2.destroy()
            return
    
        comptes = lire_compte()
        for i, (n, solde) in enumerate(comptes):
            if n == nom:
                comptes[i] = (n, solde + montant)
                ecrire_compte(comptes)
                label_result.config(text=f"✅ {montant} € déposés. Nouveau solde : {solde + montant} €")
                fenetre_creation2.destroy()
                return
                
        label_result.config(text="❌ Compte introuvable.")
        fenetre_creation2.destroy()
        
    fenetre_creation2 = tk.Toplevel(root)
    fenetre_creation2.title("faire un depot")
    fenetre_creation2.geometry("400x200")

    label_info2 = tk.Label(fenetre_creation2, text="Saisir votre nom d'utilisateur :", font=("Arial", 12))
    label_info2.pack(pady=10)
    entre_nom2 = tk.Entry(fenetre_creation2, width=30)
    entre_nom2.pack(pady=5)
    
    label_montant2 = tk.Label(fenetre_creation2, text="Saisir le montant :", font=("Arial", 12))
    label_montant2.pack(pady=10)
    entre_montant2 = tk.Entry(fenetre_creation2, width=30)
    entre_montant2.pack(pady=5)
    
    bouton_valider2 = tk.Button(fenetre_creation2, text="Valider", command=valider_depot)
    bouton_valider2.pack(pady=10)
    

# --- Retrait d'argent ---

def faire_un_retrait():
    def valider_retrait():
        nom = entre_nom3.get().strip()
        try:
            montant = float(entre_montant3.get())
        except ValueError:
            label_result.config(text="❌ Montant invalide.")
            return
    
        comptes = lire_compte()
        for i, (n, solde) in enumerate(comptes):
            if n == nom:
                if solde >= montant:
                    comptes[i] = (n, solde - montant)
                    ecrire_compte(comptes)
                    label_result.config(text=f"✅ {montant} € retirés. Nouveau solde : {solde - montant} €")
                else:
                    label_result.config(text="❌ Fonds insuffisants.")
                    fenetre_creation3.destroy()
                return
        label_result.config(text="❌ Compte introuvable.")
        fenetre_creation3.destroy()
        
    
    fenetre_creation3 = tk.Toplevel(root)
    fenetre_creation3.title("faire un retrait")
    fenetre_creation3.geometry("400x200")

    label_info3 = tk.Label(fenetre_creation3, text="Saisir votre nom d'utilisateur :", font=("Arial", 12))
    label_info3.pack(pady=10)
    entre_nom3 = tk.Entry(fenetre_creation3, width=30)
    entre_nom3.pack(pady=5)
    
    label_montant3 = tk.Label(fenetre_creation3, text="Saisir le montant :", font=("Arial", 12))
    label_montant3.pack(pady=10)
    entre_montant3 = tk.Entry(fenetre_creation3, width=30)
    entre_montant3.pack(pady=5)
    
    bouton_valider3 = tk.Button(fenetre_creation3, text="Valider", command=valider_retrait)
    bouton_valider3.pack(pady=10)

# --- transfert d'argent ---
    
def faire_un_transfert():
    def valider_transfert():
        expediteur = entre_nom5.get().strip()
        destinataire = entre_nom6.get().strip()
        try:
            montant = float(entre_montant6.get())
        except ValueError:
            label_result.config(text="❌ Montant invalide.")
            fenetre_transfert.destroy()
            return

        comptes = lire_compte()
        index_expediteur = index_destinataire = -1

        for i, (nom, solde) in enumerate(comptes):
            if nom == expediteur:
                index_expediteur = i
            if nom == destinataire:
                index_destinataire = i

        if index_expediteur == -1:
            label_result.config(text="❌ Compte expéditeur introuvable.")
        elif index_destinataire == -1:
            label_result.config(text="❌ Compte destinataire introuvable.")
        elif comptes[index_expediteur][1] < montant:
            label_result.config(text="❌ Fonds insuffisants.")
        else:
            comptes[index_expediteur] = (expediteur, comptes[index_expediteur][1] - montant)
            comptes[index_destinataire] = (destinataire, comptes[index_destinataire][1] + montant)
            ecrire_compte(comptes)
            label_result.config(text=f"✅ Transfert de {montant} € de {expediteur} à {destinataire} réussi.")

        fenetre_transfert.destroy()

    # Fenêtre de transfert
    fenetre_transfert = tk.Toplevel(root)
    fenetre_transfert.title("Faire un transfert")
    fenetre_transfert.geometry("400x300")

    label_info5 = tk.Label(fenetre_transfert, text="Nom de l'expéditeur :", font=("Arial", 12))
    label_info5.pack(pady=5)
    entre_nom5 = tk.Entry(fenetre_transfert, width=30)
    entre_nom5.pack(pady=5)

    label_info6 = tk.Label(fenetre_transfert, text="Nom du bénéficiaire :", font=("Arial", 12))
    label_info6.pack(pady=5)
    entre_nom6 = tk.Entry(fenetre_transfert, width=30)
    entre_nom6.pack(pady=5)

    label_montant6 = tk.Label(fenetre_transfert, text="Montant à transférer :", font=("Arial", 12))
    label_montant6.pack(pady=5)
    entre_montant6 = tk.Entry(fenetre_transfert, width=30)
    entre_montant6.pack(pady=5)

    bouton_valider6 = tk.Button(fenetre_transfert, text="Valider", command=valider_transfert)
    bouton_valider6.pack(pady=10)

        

# --- Interface graphique principale ---

root = tk.Tk()
root.title("BANQUE FRANCE-AFRIQUE")
root.geometry("700x650")
root.configure(bg="#DDEEFF")

texte_accueil = (
    "Bienvenue dans votre espace client !\n\n"
    "Voici les opérations disponibles :\n"
    "1 - Créer un compte : enregistrez un nouveau nom (solde initial = 0 €)\n"
    "2 - Voir le solde : consultez votre solde actuel\n"
    "3 - Faire un dépôt : ajoutez de l’argent sur votre compte\n"
    "4 - Faire un retrait : retirez de l’argent (si solde suffisant)\n"
    "5 - faire un transfert : envoyez de l'argent à un autre compte\n"
    "6 - Quitter\n"
)
label_intro = tk.Label(root, text=texte_accueil, justify="left", font=("calibri", 14), fg="red", wraplength=600)
label_intro.pack(pady=10)


label_result = tk.Label(root, text="", font=("arial", 14), fg="blue")
label_result.pack(pady=10)

frame_boutons = tk.Frame(root)
frame_boutons.pack(pady=10)

btn_creer = tk.Button(frame_boutons, text="1. Créer un compte", width=30, command=creer_compte)
btn_creer.grid(row=0, column=0, pady=5)

btn_solde = tk.Button(frame_boutons, text="2. Voir le solde", width=30, command=voir_solde)
btn_solde.grid(row=1, column=0, pady=5)

btn_depot = tk.Button(frame_boutons, text="3. Faire un dépôt", width=30, command=faire_un_depot)
btn_depot.grid(row=2, column=0, pady=5)

btn_retrait = tk.Button(frame_boutons, text="4. Faire un retrait", width=30, command=faire_un_retrait)
btn_retrait.grid(row=3, column=0, pady=5)

btn_transfert = tk.Button(frame_boutons, text="5. Faire un transfert", width=30, command=faire_un_transfert)
btn_transfert.grid(row=3, column=0, pady=5)

btn_quitter = tk.Button(frame_boutons, text="6. Quitter", width=30, command=root.destroy)
btn_quitter.grid(row=4, column=0, pady=10)

root.mainloop()
