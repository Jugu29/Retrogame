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

# Nombre de vies du vaisseau
vie_vaisseau = 3 

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
        if tir[1] + tir_hauteur < 0:  
            tirs_liste.remove(tir)

def ennemis_creation():
    """Ajoute 4 ennemis à des positions différentes toutes les secondes"""
    if pyxel.frame_count % 30 == 0:
        for _ in range(1):
            x = random.randint(0, ecran_l - 8)
            y = 0
            sprite_coordinates = random.choice([(0, 0), (0, 8), (8, 0), (8, 8)])  
            ennemis_liste.append([x, y, sprite_coordinates])

def ennemis_maj():
    """Déplace les ennemis vers le bas et les supprime s'ils sortent de l'écran"""
    for ennemi in ennemis_liste[:]:
        ennemi[1] += 1
        if ennemi[1] > ecran_h:
            ennemis_liste.remove(ennemi)

def collision(x1,  y1, l1, h1, x2, y2, l2, h2):
    if x1 <= x2+l2 and x1+l1>=x2 and y1 <= y2+h2 and y1+h1>=y2:
        return True
    return False

def gestion_collision_vaisseau():
    global ennemis_liste, vie_vaisseau
    for ennemi in ennemis_liste[:]:
        if collision(vaisseau_x, vaisseau_y, vaisseau_l, vaisseau_h, ennemi[0], ennemi[1], 8, 8):
            ennemis_liste.remove(ennemi)  
            explosions_creation(vaisseau_x, vaisseau_y)  
            vie_vaisseau -= 1
            print(vie_vaisseau)
            if vie_vaisseau <= 0:
                pyxel.quit()

def gestion_collisions():
    global ennemis_liste, tirs_liste, explosions_liste
    for tir in tirs_liste[:]:
        for ennemi in ennemis_liste[:]:
            if collision(tir[0], tir[1], tir_largeur, tir_hauteur, ennemi[0], ennemi[1], 8, 8):
                tirs_liste.remove(tir)
                ennemis_liste.remove(ennemi)
                explosions_creation(ennemi[0], ennemi[1])
                break

def explosions_creation(x, y):
    explosions_liste.append([x, y, 0])

def explosions_animation():
    for explosion in explosions_liste:
        explosion[2] +=1
        if explosion[2] == 12:
            explosions_liste.remove(explosion)

def update():
    global vaisseau_x, vaisseau_y

    vaisseau_x, vaisseau_y = vaisseau_deplacement(vaisseau_x, vaisseau_y)
    tirs_creation(vaisseau_x, vaisseau_y)
    tirs_deplacement()
    ennemis_creation()
    ennemis_maj()
    gestion_collisions()
    gestion_collision_vaisseau()
    explosions_animation()

def draw():
    pyxel.cls(0)

    # Dessin du vaisseau
    sprite_x = 0 if pyxel.frame_count % 30 == 0 else 8
    pyxel.blt(vaisseau_x, vaisseau_y, 0, sprite_x, 0, 8, 8)

    # Dessin des tirs
    for tir in tirs_liste:
        pyxel.rect(tir[0], tir[1], tir_largeur, tir_hauteur, 5)

    # Dessin des ennemis 
    for ennemi in ennemis_liste:
        pyxel.blt(ennemi[0], ennemi[1], 1, ennemi[2][0], ennemi[2][1], 8, 8)  # Utilisation des coordonnées spécifiques

    # explosions (cercles de plus en plus grands)
    for explosion in explosions_liste:
        pyxel.circb(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4), 8+explosion[2]%3)

pyxel.run(update, draw)
