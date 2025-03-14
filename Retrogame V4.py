import pyxel
import random

# Taille de la fenêtre
ecran_l = 128
ecran_h = 128

pyxel.init(ecran_l, ecran_h, title="Retro game")

# Position et taille du vaisseau
vaisseau_x = 58
vaisseau_y = 100
vaisseau_l = 8
vaisseau_h = 8

# initialisation des explosions
explosions_liste = []

# Liste des ennemis
ennemis_liste = []

# Liste des tirs
tirs_liste = []
tir_largeur = 1
tir_hauteur = 4

# Chargement des images
pyxel.load("images.pyxres")

def vaisseau_deplacement(x, y):
    if pyxel.btn(pyxel.KEY_RIGHT) and x < ecran_l - vaisseau_l:
        x += 1
    if pyxel.btn(pyxel.KEY_LEFT) and x > 0:
        x -= 1
    if pyxel.btn(pyxel.KEY_UP) and y > 0:
        y -= 1
    if pyxel.btn(pyxel.KEY_DOWN) and y < ecran_h - vaisseau_h:
        y += 1
    return x, y

def tirs_creation(x, y):
    if pyxel.btnr(pyxel.KEY_SPACE):
        tirs_liste.append([x, y])
        tirs_liste.append([x + vaisseau_l - tir_largeur, y])

def tirs_deplacement():
    for tir in tirs_liste[:]:
        tir[1] -= 2
        if tir[1] < 0:
            tirs_liste.remove(tir)

def ennemis_creation():
    """Ajoute 4 ennemis à des positions différentes toutes les secondes"""
    if pyxel.frame_count % 30 == 0:
            x = random.randint(0, ecran_l - 8)
            y = 0
            ennemis_liste.append([x, y])

def ennemis_maj():
    """Déplace les ennemis vers le bas et les supprime s'ils sortent de l'écran"""
    for ennemi in ennemis_liste[:]:
        ennemi[1] += 1
        if ennemi[1] > ecran_h:
            ennemis_liste.remove(ennemi)

def collision(x1,  y1, l1, h1, x2, y2, l2, h2):
    """
    x1:abscisse de l'objet1
    y1:ordonnée de l'objet1
    l1:largeur de l'objet1
    h1:hauteur de l'objet1
    x2:abscisse de l'objet2
    y2:ordonnée de l'objet2
    l2:largeur de l'objet2
    h2:hauteur de l'objet2
    Retourne True si collision, False sinon
    """
    if x1 <= x2+l2 and x1+l1>=x2 and y1 <= y2+h2 and y1+h1>=y2:
        return True
    return False

def explosions_creation(x, y):
    """explosions aux points de collision entre deux objets"""
    explosions_liste.append([x, y, 0])

# Mise à jour
def update():
    global vaisseau_x, vaisseau_y
    vaisseau_x, vaisseau_y = vaisseau_deplacement(vaisseau_x, vaisseau_y)
    tirs_creation(vaisseau_x, vaisseau_y)
    tirs_deplacement()
    ennemis_creation()
    ennemis_maj()

# Affichage
def draw():
    pyxel.cls(0)

    # Dessin du vaisseau
    sprite_x = 0 if pyxel.frame_count % 30 == 0 else 8
    pyxel.blt(vaisseau_x, vaisseau_y, 0, sprite_x, 0, 8, 8)

    # Dessin des tirs
    for tir in tirs_liste:
        pyxel.rect(tir[0], tir[1], tir_largeur, tir_hauteur, 5)

    # Dessin des ennemis (4 différents)
    for ennemi in ennemis_liste:
        sprite_x = 0 if pyxel.frame_count % 30 == 0 else 8
        pyxel.blt(ennemi[0], ennemi[1], 1, sprite_x, 0, 8, 8)
    # explosions (cercles de plus en plus grands)
    for explosion in explosions_liste:
        pyxel.circb(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4), 8+explosion[2]%3) 

pyxel.run(update, draw)
