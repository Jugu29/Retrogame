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

#vies du vaisseau
vie_vaisseau = 3
vie_temps = 0 

# Dessins des vies
vie_x = 100
vie_y = 100
vie_l = 7
vie_h = 6

#powerups
powerups_liste = []

#score
score = 0

def vaisseau_deplacement(x, y):
    vitesse = 1 + (score // 200) 
    if pyxel.btn(pyxel.KEY_RIGHT) and x < ecran_l - vaisseau_l:
        x += vitesse
    if pyxel.btn(pyxel.KEY_LEFT) and x > 0:
        x -= vitesse
    if pyxel.btn(pyxel.KEY_UP) and y > 0:
        y -= vitesse
    if pyxel.btn(pyxel.KEY_DOWN) and y < ecran_h - vaisseau_h:
        y += vitesse
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

def powerup_creation():
    if pyxel.frame_count % 500 == 0:
        x = random.randint(0, ecran_l - 8)
        y = 0
        sprite = random.choice([(0, 8), (8, 8)])  
        powerups_liste.append([x, y, sprite])

def powerup_deplacement():
    for powerup in powerups_liste[:]:
        powerup[1] += 1
        if powerup[1] > ecran_h:  
            powerups_liste.remove(powerup)
cadence_tir = 15  
invincible = False
invincible_timer = 0

def gestion_collision_powerup():
    global powerups_liste, cadence_tir, invincible, invincible_timer
    for powerup in powerups_liste[:]:
        if collision(vaisseau_x, vaisseau_y, vaisseau_l, vaisseau_h, powerup[0], powerup[1], 8, 8):
            powerups_liste.remove(powerup)

            
            if powerup[2] == (0, 8):
                cadence_tir = max(5, cadence_tir - 5)  
                
            
            elif powerup[2] == (8, 8):
                invincible = True
                invincible_timer = 300 


def gestion_collision_vaisseau():
    global ennemis_liste, vie_vaisseau, vie_temps 
    for ennemi in ennemis_liste[:]:
        if collision(vaisseau_x, vaisseau_y, vaisseau_l, vaisseau_h, ennemi[0], ennemi[1], 8, 8):
            ennemis_liste.remove(ennemi)
            print(score)
            explosions_creation(vaisseau_x, vaisseau_y)  
            vie_vaisseau -= 1
            vie_temps = 10 
            if vie_vaisseau <= 0:
                pyxel.quit()




def gestion_collisions():
    global ennemis_liste, tirs_liste, explosions_liste, score, vie_vaisseau
    for tir in tirs_liste[:]:
        for ennemi in ennemis_liste[:]:
            if collision(tir[0], tir[1], tir_largeur, tir_hauteur, ennemi[0], ennemi[1], 8, 8):
                tirs_liste.remove(tir)
                ennemis_liste.remove(ennemi)
                explosions_creation(ennemi[0], ennemi[1])
                score += 10  
                if score >= 1000:
                    score = 0  
                    if vie_vaisseau < 3: 
                        vie_vaisseau += 1
                break



def explosions_creation(x, y):
    explosions_liste.append([x, y, 0])

def explosions_animation():
    for explosion in explosions_liste:
        explosion[2] +=1
        if explosion[2] == 12:
            explosions_liste.remove(explosion)


def vies_vaisseau():
    global vie_temps
    if vie_temps > 0:
        vie_temps -= 1


def update():
    global vaisseau_x, vaisseau_y, invincible_timer, invincible

    vaisseau_x, vaisseau_y = vaisseau_deplacement(vaisseau_x, vaisseau_y)
    tirs_creation(vaisseau_x, vaisseau_y)
    tirs_deplacement()
    ennemis_creation()
    ennemis_maj()
    powerup_creation()
    powerup_deplacement()
    gestion_collisions()
    gestion_collision_vaisseau()
    gestion_collision_powerup()
    explosions_animation()
    vies_vaisseau()
    if invincible:
        invincible_timer -= 1
        if invincible_timer <= 0:
            invincible = False


def draw():
    pyxel.cls(0)

    # Vaisseau
    pyxel.blt(vaisseau_x, vaisseau_y, 0, 0, 0, 8, 8)

    # Tirs
    for tir in tirs_liste:
        pyxel.rect(tir[0], tir[1], tir_largeur, tir_hauteur, 5)

    # Ennemis 
    for ennemi in ennemis_liste:
        pyxel.blt(ennemi[0], ennemi[1], 1, ennemi[2][0], ennemi[2][1], 8, 8) 

    # Explosions 
    for explosion in explosions_liste:
        pyxel.circb(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4), 8+explosion[2]%3)

    # Affichage des vies
    for i in range(3):
        if i < vie_vaisseau:
            pyxel.blt(100 + i * 10, 10, 2, 0, 0, 8, 8)  
        elif i == vie_vaisseau and vie_temps > 0:
            pyxel.blt(100 + i * 10, 10, 2, 8, 0, 8, 8)  


    # Affichage score
    pyxel.text(5, 5, f"Score: {score}", 7)

    # Affichage vies
    for i in range(5): 
        if i < vie_vaisseau:
            pyxel.blt(100 + i * 10, 10, 2, 0, 0, 8, 8)  
        elif i == vie_vaisseau and vie_temps > 0:
            pyxel.blt(100 + i * 10, 10, 2, 8, 0, 8, 8)
    # Affichage des power-ups
    for powerup in powerups_liste:
        pyxel.blt(powerup[0], powerup[1], 2, powerup[2][0], powerup[2][1], 8, 8)


pyxel.run(update, draw)
