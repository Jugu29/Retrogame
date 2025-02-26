import pyxel

# taille de la fenetre 128x128 pixels
# ne pas modifier
pyxel.init(128, 128, title="Retro game")

# position initiale du vaisseau
# (origine des positions : coin haut gauche)
vaisseau_x = 60
vaisseau_y = 60
vaisseau_l = 8
vaisseau_h = 8
# chargement des images
pyxel.load("images.pyxres")
def vaisseau_deplacement_Droite_Gauche(x, y):
   """déplacement avec les touches de directions"""

   if pyxel.btn(pyxel.KEY_RIGHT) and x < 127 - vaisseau_l:
       x = x + 1
       
   if pyxel.btn(pyxel.KEY_LEFT) and x > 0:
       x = x - 1
   
   return x, y # retourne les coordonnées mise à jour

def vaisseau_deplacement_Bas_Haut(x, y):
   """déplacement avec les touches de directions"""

   if pyxel.btn(pyxel.KEY_UP) and y > 0:
       y = y - 1
   if pyxel.btn(pyxel.KEY_DOWN) and y < 127 - vaisseau_l:
       y = y + 1
   return x, y # retourne les coordonnées mise à jour


# initialisation des tirs
tirs_liste = []

def tirs_creation(x, y, tirs_liste):
    """création d'un tir avec la barre d'espace"""
    # btnr pour eviter les tirs multiples
    if pyxel.btnr(pyxel.rect):
        tirs_liste.append([x, y])
    return tirs_liste



# =========================================================
# == UPDATE
# =========================================================
def update():
   """mise à jour des variables (30 fois par seconde)"""

   global vaisseau_x, vaisseau_y, vaisseau_l, vaisseau_h
   vaisseau_x, vaisseau_y = vaisseau_deplacement_Droite_Gauche(vaisseau_x, vaisseau_y)
   vaisseau_x, vaisseau_y = vaisseau_deplacement_Bas_Haut(vaisseau_x, vaisseau_y)
   
   # creation des tirs en fonction de la position du vaisseau
   #tirs_liste = tirs_creation(_______________, _____________, _______________)

# =========================================================
# == DRAW
# =========================================================
def draw():
   """dessin des objets (30 fois par seconde)"""

   # vide la fenetre
   pyxel.cls(0)

   # vaisseau (carre 8x8)
   # x, y, largeur, hauteur, couleur
   pyxel.blt(vaisseau_x, vaisseau_y, 0, 0, 0, 8, 8)
    # tirs
   for tir in tirs_liste: # je boucle sur ma liste de tirs
        pyxel.rect(tir[0], tir[1], 1, 4, 10) #je dessine un rectangle



# lance le programme principal
pyxel.run(update, draw)

