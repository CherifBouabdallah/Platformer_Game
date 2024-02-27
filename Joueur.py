import pgzrun
import time
from pgzhelper import *
from Parametre import *
from Monde import *


''' Cette classe définie mes personnages.
     Elle comprend l'ensemble des méthodes qui leurs sont appliquées '''

class Joueur(): 

    ## Initialisation, j'ai besoin du paramètre actor (type particulier défini par pygame zero)

    def __init__(self, actor, scale=1, name="alien"):
        self.actor=actor # paramètre actor de pygame zero
        self.gauche=False # Est-ce que le regard du personnage est à gauche ou a droite 
        self.scale=scale # mise à l'échelle de l'image du joueur 
        self.vitesse=0 # vitesse verticale du personnage 
        self.vivant=True # Est-ce qu'il est encore vivant
        self.actor.scale=scale # Permet de gérer la taille de l'image du personnage
        self.name=name # Nom de l'image
        self.jump_count = 0
        self.max_jump = 2

    ## Cette méthode permet l'affichage d'une image à taille voulu. 
    ## Il y a deux options
    # 1. Définir une échelle ( un facteur multiplicatif: 2 veut dire 2fois plus grande)
    # 2. Définir une taille. Mettre scale à 0 et donner des valeurs pour transform

    def image(self,name, scale, transform=(pixel/2,pixely/2)):
        if scale!=0:
            self.actor.image=name
            self.actor.scale=scale
        elif transform!=(0,0):
            self.actor.image=name
            self.actor._surf = pygame.transform.scale(self.actor._surf, transform)



    ## Méthode de déplacement d'un personnage. Il ne tient en compte de rien. 
    ## Il avance à chauqe itération  

    def deplacement_volant(self):
        self.actor.left += 3  # déplace le self de 3 pixel vers la gauche
        if self.actor.left > WIDTH: # Si le  personnage sort de l'écran. 
            self.actor.right = 0 # Il revient au début


    ## Méthode de déplacement d'un personnage au sol. 
    ## Il tient compte: 
        # 1. Du sol 
        # 2. De la gravité
        # 3. Des touches claviers 

    def deplacement_rampant(self, ennemy, keyboard, animate, sounds, clock):
        L_monde=monde_rect() # Création du monde 
      
        # définition des variables de déplacement
        dx=0 # Pas de déplacement de base horizontal
        # dy=2 # Déplacement uniforme on tient pas compte de la gravité
      
        # Si on veut tenir compte de la gravité 
        self.vitesse+=gravity # On fait augmenter la vitesse de chute 
        dy=self.vitesse # On déplace de la vitesse

        # gestion des déplacements
        if keyboard.left: # Gestion de la touche clavier "left"
            dx=-8
            self.gauche=True # Il regarde à gauche 
        if keyboard.right: # Gestion de la touche clavier "right"
            dx=8
            self.gauche=False  # Il regarde à droite

        if self.actor.right < 0: # Si le  personnage sort de l'écran coté gauche. 
            self.actor.right = WIDTH # Il revient au coté droit
        if self.actor.left+dx > WIDTH: # Si le  personnage sort de l'écran. 
            self.actor.left = 0 # Il revient au début

        
        # Gestion des collisions avec le monde 
        for bloc in L_monde:
                #collision verticale: on regarde si la future position va rentrer en conflit avec un bloc  du monde
                if bloc[1].colliderect(self.actor.left, self.actor.top+dy, self.actor.width, self.actor.height):
                    dy=0 # Si il y a conflit/ collision on bouge pas 
                    self.vitesse=0 # On remet la vitesse à 0 
                    if bloc[2]==2: # On regarde si le bloc est de la lave. Si c'est de la lave. Le joueur meurt 
                        self.set_alien_death(sounds,animate,clock, dev_mode)
                #collision horizontale: on regarde les collision horizontale
                if bloc[1].colliderect(self.actor.left+dx, self.actor.top, self.actor.width, self.actor.height):
                    dx=0
        
        
        #if self.actor.colliderect(ennemy.actor.left, ennemy.actor.top, ennemy.actor.width, ennemy.actor.height):
        #    self.set_alien_death(sounds,animate,clock, dev_mode)

    
        # Gestion de la touche clavier "up"
        if keyboard.space or keyboard.up:
            if dy== 0: #or self.jump_count < self.max_jump: # Si il est au sol
                self.vitesse = -15
                self.jump_count += 1

        if dy == 0:
            self.jump_count = 0


        # Une fois que l'on sait de combien on se déplace, on fait effectivement les déplacement    
        self.actor.x +=dx # déplacement en x 
        self.actor.bottom+=dy # déplacment en y ( j'utilise la propriété bottom, le bas du personnage)

    # Défini la réaction du personnage si on le blesse
    def set_alien_hurt(self, sounds, clock): 
        self.image('alien_hurt',self.scale)  # change l'image
        sounds.eep.play() # joue le son eep 
        clock.schedule_unique(self.set_alien_normal, 1.0) # Rechange l'image au bout de 1s 

    # On revient à l'image normale
    def set_alien_normal(self): 
        if self.gauche:
            self.image('alien_g',0)
        else: 
            self.image('alien',self.scale)


    def DEV_MODE(self, keyboard, dev_mode): #cette fonction va me permettre d'etre invincible
        if keyboard.k:
            dev_mode = True
            self.topright = 0, 0
            print('DEV_MODE on')

        if keyboard.l:
            dev_mode = False
            print('DEV_Mode off')
            print(dev_mode)

        #print(dev_mode)    
        return dev_mode
    
    # Défini ce qui se passe si l'alien meurt
    def set_alien_death(self, sounds,animate, clock, dev_mode):
        if not dev_mode:
            self.image('alien_hurt',self.scale) 
            sounds.death.play()
            animate(self.actor, tween="decelerate", pos=(self.actor.pos[0],1000))
            clock.schedule_unique(self.set_alien_normal, 1.0)
            self.vivant = False
        

            
class Ennemy(Joueur): #code repris du cours. héritage
    def __init__(self, actor, scale=1, name="ennemy"):
        super().__init__(actor, scale, name)

    def deplacement_rampant(self, dy, sounds, animate, clock):
        L_monde=monde_rect() # Création du monde 
        # définition des variables de déplacement
        dx = 5
        
        if self.gauche == True:
            dx = -5
        else:
            dx = 5


        # Si on veut tenir compte de la gravité 
        self.vitesse+=gravity # On fait augmenter la vitesse de chute 
        dy=self.vitesse # On déplace de la vitesse

        if self.actor.right < 0: # Si le  personnage sort de l'écran coté gauche. 
            self.actor.right = WIDTH # Il revient au coté droit
        if self.actor.left+dx > WIDTH: # Si le  personnage sort de l'écran. 
            self.actor.left = 0 # Il revient au début

        for bloc in L_monde:
            #collision verticale: on regarde si la future position va rentrer en conflit avec un bloc  du monde
            if bloc[1].colliderect(self.actor.left, self.actor.top+dy, self.actor.width, self.actor.height):
                dy=0 # Si il y a conflit/ collision on bouge pas 
                self.vitesse=0 # On remet la vitesse à 0 
                if bloc[1].colliderect(self.actor.left, self.actor.top, self.actor.width, self.actor.height):
                    if dx < 0:
                        dx = 5
                    else:
                        dx = -5


        self.actor.bottom += dy           
        self.actor.left += dx
        # gestion des déplacements
        if dx < 0: # Gestion de la direction
            self.gauche=True # Il regarde à gauche 
        else: # Gestion de la direction
            self.gauche=False  # Il regarde à droite
        if self.gauche:
            self.image('ennemy_g',self.scale)
        else: 
            self.image('ennemy',self.scale)


    def set_ennemy_death(self, sounds, animate, dev_mode, alien, clock):

        if alien.actor.left <= self.actor.right and alien.actor.right >= self.actor.left and alien.actor.bottom >= self.actor.top-6 and alien.actor.bottom <= self.actor.top: #code inspiré de jonathan !
            sounds.death.play()
            animate(self.actor, tween="decelerate", pos=(self.actor.pos[0],1000))
            self.vivant = False
        
        if alien.actor.left <= self.actor.right and alien.actor.right >= self.actor.left and alien.actor.top >= self.actor.top-6:
            alien.set_alien_death(sounds, animate, clock, dev_mode)

