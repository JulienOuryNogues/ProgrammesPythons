__author__ = 'Julien'

from tkinter import *
from random import randrange
from tkinter.ttk import *
from tkinter import ttk

#Grace à un système de sauvegarde dans un fichier txt, j'obtiens le meilleur score, que je modifie

def get_best_score():
  global bestscore
  try:

    f=open("scores.txt","r")
    res=0
    e=f.readline()
    while e!="":
        try:
            res=int(e)
        except:
            ()
        e=f.readline()
    bestscore=res
    f.close()

  except:
    bestscore=0
    f=open("scores.txt","w")
    f.write("Historique des meilleurs scores ! :) \n")
    f.close()


#pour une liste, prend son dernier élément et le place en tête

def permute (l):
    n=len(l)
    a=l[n-1]
    return [a]+l[:(n-1)]


# ne fait rien, pour désactiver un bouton

def rien (event=0):
    ()

def move():
    #déplacement du snake
    global x1, y1, dx, dy, jeu,pions,cible,coords,peut_jouer,score,sco,sco2,br
    n=len(pions)
    peut_jouer=True
    x1, y1 = x1 +dx, y1 + dy

    if x1 >480 or y1>480 or x1<0 or y1<0 or (x1,y1)in coords:
        #Condition de défaite (toucher des bords) et le serpent se recoupe
        stop_it()
        sco.destroy()
        sco2=Label(fen,text="Score final : "+str(score))
        sco2.grid(row=3,column=0)
        sco=Label(fen,text=" Vous avez perdu ! :( ")
        sco.grid(row=4,column=0,columnspan=2)
        #On enregistre le meilleur score
        enregistre()
        # je réactive le bouton restart
        br.config(command=restart)
    if x1==xcible and y1==ycible: #Condition de manger le pion
        #Si la cible est mangée, il faut aggrandir le serpent
        pions= [can.create_oval(xcible, ycible, xcible+20, ycible+20, width=2, fill='green')] + pions
        coords=[(xcible,ycible)]+coords
        #on déplace enfin la cible
        deplace_cible()
        n=n+1
        score=score+1
        sco.destroy()
        sco=Label(fen,text="Votre score est de : "+str(score))
        sco.grid(row=3,column=0)

    else:
        # je prends le dernier de la liste que je mets en tête
        #ATTENTION, pour le cas n=1, il faut incrémenter manuellement les coordonnées
        can.coords(pions[n-1],x1,y1,x1+20,y1+20) #Pour faire avancer le snake
        pions=permute(pions)
        # Pour incrémenter les coordonnées, je prends la tête, je la stocke en a.
        #  Je prends ensuite tous les élements de coords sauf le dernier (c'est L) et je renvoie [a]+L
        coords=incremente(coords,x1,y1)
    if n==625:
        #Condition de victoire ! remplissage total du screen (serpent de taille 25*25)
        stop_it()
        sco.destroy()
        sco2=Label(fen,text="Score final : "+str(score))
        sco2.grid(row=3,column=0)
        sco=Label(fen,text=" Incroyable ! Vous avez réussi ! :D Toutes mes Félicitations !!")
        sco.grid(row=4,column=0,columnspan=2)
        #On enregistre le meilleur score
        enregistre()
        # je réactive le bouton restart
        br.config(command=restart)

    if jeu:
        fen.after(vit,move)

 # => boucler après vit(choisi par l'utilisateur)  millisecondes


def enregistre():
    global score,bestscore
    if score>bestscore:
        f=open("scores.txt","r")  #je prends tout pour tout recopier
        tout=f.read()
        f.close()
        f=open("scores.txt","w")
        f.write(tout+"\n")
        f.write(str(score))
        f.close()




#fait l'incrémentation sus-mentionnée

def incremente(l,x1,y1):
    k=len(l)
    return [(x1,y1)]+l[:(k-1)]



# EN CAS D'INTERACTION AVEC L'UTILISATEUR


#Arrêt du jeu si on le demande (bouton)

def stop_it():
    # Stoppe le jeu
    global jeu
    jeu =False
    can.bind("<Key>",rien)



def direction(event): #Quand on appuie sur une touche, on change le prochain pas (ie) le dx ou le dy
    global x,y,dx,dy,jeu,debut,peut_jouer,scoR,br
    jeu=True
    br.config(command=rien)
    touche = event.keysym
    # déplacement vers le haut
    # Dans chaque cas, je vais interdire au snake de faire demi-tour (ce qui normalement cause le game-over)
    #J'enlève aussi le cas ou le joueur appuie sur la même touche que la direction d'avancée.
    # Car sinon il jouerait dans le vide
    if peut_jouer:
      if touche == 'Up':
        if dy==0: # Si je n'allais pas en arrière, ni en avant, alors OK
            dy = -20  #Attention au repère de python qui est à l'envers
            dx = 0
            peut_jouer=False  # On enlève alors la possibilité de jouer au joueur
        #Sinon je ne fais rien
    # déplacement vers le bas
      if touche == 'Down':
        if dy==0: #Si je n'allais pas en avant, ni en arrière , alors c'est OK
            dy = 20
            dx = 0
            peut_jouer=False  # On enlève alors la possibilité de jouer au joueur
    # déplacement vers la droite
      if touche == 'Right':
        if dx==0: #Si je n'allais pas à gauche, ni à droite, alors OK
            dx = 20
            dy = 0
            peut_jouer=False  # On enlève alors la possibilité de jouer au joueur
    # déplacement vers la gauche
      if touche == 'Left':
        if dx==0: #Si je n'allais pas droite, ni à gauche, alors OK
            dx = -20
            dy = 0
    if debut and (touche=="Left" or touche=="Right" or touche=="Up" or touche=="Down") :
        #Si on est au départ, on lance le move ! Sinon cela ne sert à rien sauf accélérer le truc
        debut=False #On n'y est plus !
        move()
        cree_cible()




# EN CAS DE MANGEAGE DE CIBLE

#Creer une pièce à manger.


def cree_cible():
    global fen,can,xcible,ycible,cible,coords
    i=randrange(24)
    j=randrange(24)
    while (i*20,j*20)in coords: #on choisit une cible qui n'est pas "sur" le snake
        i=randrange(24)
        j=randrange(24)
    xcible=i*20
    ycible=j*20
    cible=can.create_rectangle(xcible+3,ycible+3,xcible+13,ycible+13,fill="red",outline="black")


#Changer la cible de place si on la mange

def deplace_cible():
    global fen,can,xcible,ycible,xcible
    i=randrange(24)
    j=randrange(24)
    while (i*20,j*20)in coords: #on choisit une cible qui n'est pas "sur" le snake
        i=randrange(24)
        j=randrange(24)
    xcible=i*20
    ycible=j*20
    can.coords(cible,xcible+3,ycible+3,xcible+13,ycible+13)


#Définition de la vitesse de jeu par l'utilisateur


def lent():
    global vit
    vit =75 #avancée toutes les 200 ms
    depart()

def moyen():
    global vit
    vit=50
    depart()

def rapide():
    global vit
    vit=30
    depart()

def dement():
    global vit
    vit=20
    depart()





# définit un restart, en fait une (ré)initialisation des variables

def restart():
    global x1,y1,dx,dy,xcible,ycible,score,bestscore,pions,coords,debut,jeu,peut_jouer,pion,can,b1,br,hist,sco,sco2,bm
    """if jeu:  # En cas de restart en cours de jeu, on provoque le GameOver
        stop_it()
        sco.destroy()
        sco=Label(fen,text=" Vous avez restart ! ")
        sco.pack(anchor="center",pady=150)
        sco2=Label(fen,text="Score final : "+str(score))
        sco2.pack(anchor="center")
        #On enregistre le meilleur score
        enregistre()"""  # Devenu inutile, car je gèle le bouton en jeu. mais je le laisse au cas ou
    try:  #J'essaie de détruire tout sauf la fenêtre (cas d'un restart et pas d'un start)
        can.destroy()
        b1.destroy()
        br.destroy()
        bm.destroy()
        hist.destroy()
        sco.destroy()
        sco2.destroy()
    except: #Sinon je suis dans le start, il y a rien à détruire
        ()
    x1, y1 = 240, 240 # coordonnées initiales
    dx, dy = 0, 0 # 'pas' du déplacement
    #initialisation obligatoire de la cible
    xcible=0
    ycible=0
    #Le score
    score =0
    # Quelques variables booléennes
    debut =True # Variable qui dit si on est au début
    peut_jouer=True # On se débrouille pour que le joueur ne puisse donner qu'un ordre entre chaque pas,
    # sinon le serpent peut se mordre la queue
    bestscore=0  #On récupère le meilleur score
    get_best_score()
    can = Canvas(fen,bg='ivory',height=500, width=500)    #Aire de jeu
    can.grid(row=0,column=0,rowspan=3,columnspan=2)
    can.focus_set()
    can.bind("<Key>",direction)
    #Mon snake commence par être un cercle vert
    pion=can.create_oval(x1,y1,x1+20,y1+20, width=2, fill='green')
    pions=[pion] # Mon Snake sera une liste de boules rouges
    coords=[(x1,y1)] #Je stocke les coordonnées de chaque boule dans cette liste
    #Boutons habituels
    bm=Button(fen,text="Menu",command=menu)
    bm.grid(row=0,column=2)
    br=Button(fen,text="Restart",command=restart)
    br.grid(row=1,column=2)
    b1 = Button(fen,text='Quitter', width =8, command=fen.destroy)
    b1.grid(row=2,column=2)
    #Interface texte
    sco=Label(fen,text="Votre score est de : "+str(score))
    sco.grid(row=3,column=0)
    hist=Label(fen,text="Meilleur score : "+str(bestscore))
    hist.grid(row=3,column=1)







#========== Programme principal =============

def depart():
    global jeu,fen,fen1
    fen1.destroy() # je détruis la fenêtre de menu
    jeu =False # commutateur, dit si on est en jeu ou pas
    fen = Tk()
    fen.title("Snake")
    restart()
    # démarrage du jeu:
    fen.mainloop()


# MENU PRINCIPAL

def menu():
    global fen1
    try: # je détruis la fenpetre de jeu en cas d'un passage jeu -> menu
        fen.destroy()
    except:
        ()
    fen1=Tk()
    fen1.title("Jeu du Snake")
    bienv=Label(text="Bienvenue au jeu du Snake ! :)" )
    bienv.grid(row=0,column=0,columnspan=2)
    diff=Label(text="Choisissez votre vitesse de jeu : ")
    diff.grid(row=1,column=0,columnspan=2)
    b1 = Button(fen1,text='Lente', command=lent)
    b1.grid(row=2,column=0)
    b2=Button(fen1,text="Moyenne",command=moyen)
    b2.grid(row=2,column=1)
    b3 = Button(fen1,text='Rapide', command=rapide)
    b3.grid(row=3,column=0)
    b4=Button(fen1,text="Démentielle",command=dement)
    b4.grid(row=3,column=1)
    mess=Label(text="Signalez-moi bugs et remarques s'il vous plait ! Bon jeu !")
    mess.grid(row=4,column=0,columnspan=2)
    b5 = Button(fen1,text='Quitter', width =8, command=fen1.destroy)
    b5.grid(row=5,column=0,columnspan=2)
    fin=Label(text="© Julien Oury--Nogues")
    fin.grid(row=6,column=0,columnspan=2)

    fen1.mainloop()


#c'est parti !

menu()