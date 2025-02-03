import pyxel
import random

# taille de la fenêtre 128x128 pixels
pyxel.init(128, 128, title="Retro game")

# Position et taille du vaisseau
vaisseau_x = 60
vaisseau_y = 60
vaisseau_l = 8
vaisseau_h = 8

# Initialisation des tirs
tirs_liste = []
tir_largeur = 1
tir_hauteur = 4

# Chargement des images
pyxel.load("images.pyxres")

def vaisseau_deplacement_Droite_Gauche(x, y):
    """Déplacement avec les touches de directions"""
    if pyxel.btn(pyxel.KEY_RIGHT) and x < 127 - vaisseau_l:
        x += 1
    if pyxel.btn(pyxel.KEY_LEFT) and x > 0:
        x -= 1
    return x, y  # retourne les coordonnées mises à jour

def vaisseau_deplacement_Bas_Haut(x, y):
    """Déplacement avec les touches de directions"""
    if pyxel.btn(pyxel.KEY_UP) and y > 0:
        y -= 1
    if pyxel.btn(pyxel.KEY_DOWN) and y < 127 - vaisseau_h:
        y += 1
    return x, y  # retourne les coordonnées mises à jour

def tirs_creation(x, y, tirs_liste):
    """Création d'un tir avec la barre d'espace"""
    # btnr pour éviter les tirs multiples
    if pyxel.btnr(pyxel.KEY_SPACE):
        tirs_liste.append([x, y])
    return tirs_liste

def tirs_deplacement(tirs_liste):
    """Déplacement des tirs vers le haut et suppression s'ils sortent du cadre"""
    for tir in tirs_liste[:]:  # Copie de la liste pour éviter les erreurs de suppression
        tir[1] -= 2  # Le tir monte
        if tir[1] < 0:  # Si le tir sort de l'écran
            tirs_liste.remove(tir)  # On le supprime
    return tirs_liste

# =========================================================
# == UPDATE
# =========================================================
def update():
    """Mise à jour des variables (30 fois par seconde)"""
    global vaisseau_x, vaisseau_y, tirs_liste

    # Déplacement du vaisseau
    vaisseau_x, vaisseau_y = vaisseau_deplacement_Droite_Gauche(vaisseau_x, vaisseau_y)
    vaisseau_x, vaisseau_y = vaisseau_deplacement_Bas_Haut(vaisseau_x, vaisseau_y)

    # Création des tirs en fonction de la position du vaisseau
    tirs_liste = tirs_creation(vaisseau_x + vaisseau_l // 2, vaisseau_y, tirs_liste)

    # Mise à jour des positions des tirs
    tirs_liste = tirs_deplacement(tirs_liste)

# =========================================================
# == DRAW
# =========================================================
def draw():
    """Dessin des objets (30 fois par seconde)"""
    pyxel.cls(0)  # Vide la fenêtre

    # Vaisseau (image 8x8)
    pyxel.blt(vaisseau_x, vaisseau_y, 0, 0, 0, 8, 8)

    # Dessin des tirs
    for tir in tirs_liste:
        pyxel.rect(tir[0], tir[1], tir_largeur, tir_hauteur, 10)  # Rectangle du tir

# Lancement du programme principal
pyxel.run(update, draw)