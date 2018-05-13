__author__ = 'Julien'

from tkinter import *

from random import randrange
from tkinter.ttk import *
from tkinter import ttk

def cercle (x, y, r, interne = "ivory", coul = "blue"):
    #Cercle de centre (x,y) et de rayon r

    cadre.create_oval(x-r,y-r,x+r,y+r,fill= interne, outline=coul)


# Je vais faire un Canvas de taille 300*300, ainsi le découpage sera simple.


M=[[0,0,0],[0,0,0],[0,0,0]]  #Matrice qui représentera le jeu

Joueur = 1 # Indique à qui est le tour

Premiercoup = 1 # A chaque restart on change de premier joueur

#Initialisation des scores

score1 = 0
score2 = 0

def case (x,y): #A partir des coordonnées cliquées, je dis à quelle case cela réfère, simplifié par mon choix de taille
    return (x//100,y//100)

def est_vide(i,j):  # Dit si la case est vide
    return M[i][j]==0


def dessine_cercle (i,j):  # Dessine un cercle au centre de la case i j
    cercle (50+i*100,50+j*100,45)


def dessine_croix (i,j): # Dessine une croix au centre de la case i j
       cadre.create_line(100*i,100*j,100*(i+1),100*(j+1), fill="red")
       cadre.create_line(100*i,100*(j+1),100*(i+1),100*j, fill="red")

def quadrillage () : # Dessine le quadrillage de base du Morpion
    global cadre
    cadre.create_line(100,0,100,300, fill="black")
    cadre.create_line(200,0,200,300, fill="black")
    cadre.create_line(0,200,300,200, fill="black")
    cadre.create_line(0,100,300,100, fill="black")

def est_match_nul(): # Dit si il reste des coups a jouer ou non. détermine la partie nulle
    res=True
    for i in range(0,3):
      for j in range(0,3):
        res = res and not(est_vide(i,j))

    return res


def est_victoire ():  # Dit s'il y a victoire d'un joueur et retourne le numéro du joueur dans un Tuple
    if M[0][0]==M[0][1] and M[0][1]==M[0][2] and M[0][0]!=0 :  #On vérifie les lignes
        return (True,M[0][0])
    elif M[1][0]==M[1][1] and M[1][1]==M[1][2] and M[1][0]!=0:
        return (True,M[1][0])
    elif M[2][0]==M[2][1] and M[2][1]==M[2][2] and M[2][0]!=0:
        return (True,M[2][0])
    elif M[0][2]==M[1][2] and M[1][2]==M[2][2] and M[0][2]!=0: # On vérifie les colonnes
        return (True,M[0][2])
    elif M[0][1]==M[1][1] and M[1][1]==M[2][1] and M[0][1] !=0:
        return (True,M[0][1])
    elif M[0][0]==M[1][0] and M[1][0]==M[2][0] and M[0][0] !=0:
        return (True,M[0][0])
    elif M[0][0]==M[1][1] and M[1][1]==M[2][2] and M[0][0] !=0: # On vérifie les diagonales
        return (True,M[0][0])
    elif M[0][2]==M[1][1] and M[1][1]==M[2][0] and M[0][2] !=0:
        return (True,M[0][2])
    else:
        return (False,0)


def stop (event):  # Fonction qui ne fait rien. Permet de désactiver le "clic" en fin de partie !
    ()



def victoire ():   # S'active en cas de victoire
    global aqui,cadre,score1,score2,scor1,scor2
    V=(est_victoire())
    J=V[1]
    if J==1:   #On incrémente le score
        score1=score1+1
    else:
        score2=score2+1
    aqui.destroy()   # On écrit l'event de victoire
    aqui=Label(fen, text="Victoire du joueur "+str(J) +" !")
    aqui.grid(row=4,column=0,columnspan=2)
    cadre.bind("<Button-1>",stop)   # On désactive le clic grace à stop
    scor1.destroy()
    scor2.destroy()
    scor1=Label(fen, text="Joueur 1 : "+str(score1) )  # On affiche les scores
    scor1.grid(row=5,column=0)
    scor2=Label(fen, text="Joueur 2 : "+str(score2) )
    scor2.grid(row=5, column=1)





def match_nul ():  # s'active en cas de match nul
    global aqui,cadre
    aqui.destroy()   # On écrit l'event de match nul
    aqui=Label(fen, text="Match nul ! Personne ne gagne de points")
    aqui.grid(row=4,column=0,columnspan=2)
    cadre.bind("<Button-1>",stop)   # On désactive le clic grâce à stop





def restart ():    # S'active par l'utilisateur avec le bouton restart
    global M,hist,aqui,Player,cadre,Premiercoup,Joueur,score2,score1,scor1,scor2
    if not((est_victoire())[0]) and not(est_match_nul()) and A==1:  #Pénalité pour restart intempestif :P
        if Joueur==1:
            score2=score2+1
            scor2.destroy()
            scor2=Label(fen, text="Joueur 2 : "+str(score2) )
            scor2.grid(row=5,column=1)
        else:
            score1=score1+1
            scor1.destroy()
            scor1=Label(fen, text="Joueur 1 : "+str(score1) )
            scor1.grid(row=5, column=0)


    M=[[0,0,0],[0,0,0],[0,0,0]]       #On remet la matrice à zéro
    Joueur = 2*Premiercoup % 3        #Je décide que dans ce cas, le joueur passe la main
    Premiercoup = 2*Premiercoup % 3   #Et on change de joueur qui entame
    hist.destroy()                    #On reset les events de jeu
    aqui.destroy()
    hist=Label(fen, text="La partie vient de commencer !")
    hist.grid(row=3,column=0,columnspan=2)
    aqui=Label(fen, text="Au tour du Joueur "+str(Joueur))
    aqui.grid(row=4,column=0,columnspan=2)
    cadre.delete(ALL)
    if A==1:   # 1 joueur             # Lors d'un restart, il faut choisir le pointeur qui correspond à notre
                                            # partie ie 1 ou 2 joueurs
      cadre.bind("<Button-1>", pointeur1)
    else:   # 2 joueurs
      cadre.bind("<Button-1>", pointeur2)
    quadrillage()
    if Premiercoup==2 and A==1:   # Il faut faire jouer l'ordi si jamais c'est lui qui commence et si on joue bien seul
        ordi()


def pointeur2 (event):  # Voici un programme pointeur qui gère deux joueurs, chacun son tour
  global Joueur,hist,aqui,fen,M
  aqui.destroy()
  hist.destroy()
  T= case(event.x,event.y)  #On récupère le clic joué
  (i,j)=T
  if not(est_vide(i,j)):  #Si on ne peut pas jouer la, bah on l'indique au joueur ;)
      hist=Label(fen, text= "Impossible de jouer en "+str(T)+": case déjà jouée")
      hist.grid(row=3,column=0,columnspan=2)
      aqui=Label(fen, text="Au tour du Joueur "+str(Joueur))
      aqui.grid(row=4,column=0,columnspan=2)
  else:  # Sinon il joue
    M[i][j]=Joueur  # On l'indique dans notre matrice
    if Joueur==1:   #On choisit la forme à dessiner selon le joueur
      dessine_croix(i,j)
    else:
      dessine_cercle(i,j)

    hist=Label(fen, text="Joueur "+str(Joueur) +" joue en "+str(T))   #On actualise notre petit historique
    hist.grid(row=3,column=0,columnspan=2)
    Joueur=2*Joueur % 3  #On change de joueur qui a la main
    aqui=Label(fen, text="Au tour du Joueur "+str(Joueur)) #Et ob l'indique
    aqui.grid(row=4,column=0,columnspan=2)



  if (est_victoire())[0]:   # On vérifie à chaque coup si on est dans une condition de fin : victoire ou nul
      victoire()
  elif est_match_nul():
      match_nul()







def pointeur1 (event):  #Pointeur qui gère une IA ordi()
  global Joueur,hist,aqui,fen,M
  Joueur=1    #J'ai codé mon programme de telle façon qu'on est toujours au Joueur 1 ici
  aqui.destroy()
  hist.destroy()
  T= case(event.x,event.y)  #On recueille ce que le joueur joue
  (i,j)=T

  if not(est_vide(i,j)): #De même, on indique si on ne peut pas jouer la
      hist=Label(fen, text= "Impossible de jouer en "+str(T)+": case déjà jouée")
      hist.grid(row=3,column=0,columnspan=2)
      aqui=Label(fen, text="Au tour du Joueur "+str(Joueur))
      aqui.grid(row=4,column=0,columnspan=2)
  else:  # Sinon il joue.
    M[i][j]=Joueur
    dessine_croix(i,j)
    hist=Label(fen, text="Joueur "+str(Joueur) +" joue en "+str(T)) #Historique actualisé
    hist.grid(row=3,column=0,columnspan=2)
    Joueur=2*Joueur % 3 #On change le joueur
    aqui=Label(fen, text="Au tour du Joueur "+str(Joueur))
    aqui.grid(row=4,column=0,columnspan=2)
    if (est_victoire())[0]:  # Avant de donner la main au CPU, on vérifie si on n'est pas dans une fin de partie
      victoire()
    elif est_match_nul():
      match_nul()
    else:  #Enfin, on le laisse jouer
      ordi ()




def ordi ():  # Programme qui fait jouer le CPU
    global hist, aqui,fen,Joueur,M
    aqui.destroy()
    hist.destroy()
    (i,j)= evalu ()  # On utilise la fonction d'évaluation définie juste après
    M[i][j]=Joueur  # On l'indique dans la matrice
    dessine_cercle(i,j) #On dessine son coup
    hist=Label(fen, text="Joueur "+str(Joueur) +" joue en "+str((i,j))) #Historique actualisé
    hist.grid(row=3,column=0,columnspan=2)
    Joueur=1 # On redonne la main au joueur
    aqui=Label(fen, text="Au tour du Joueur "+str(Joueur)) #On lui dit !
    aqui.grid(row=4,column=0,columnspan=2)
    if (est_victoire())[0]:  #Conditions de fin de partie
      victoire()
    elif est_match_nul():
      match_nul()





# Tous ces programmes sont relatifs à l'IA et la fonction d'évaluation


def combien_ligne (j,i):  # Dit combien il y a d'occurrences de cases jouées par j dans la ligne i

    res=0
    for k in range(0,3):
        if M[i][k]==j:
            res=res+1
    return res


def combien_col (j,i) : # Dit combien il y a d'occurrences de cases jouées par j dans la colonne i
    res=0
    for k in range(0,3):
        if M[k][i]==j:
            res=res+1
    return res


def combien_diag1 (j): # Dit combien il y a d'occurrences de cases jouées par j dans la daigonale principale
    res=0
    for k in range(0,3):
        if M[k][k]==j:
            res=res+1
    return res


def combien_diag2 (j): # Dit combien il y a d'occurrences de cases jouées par j dans l'anti-diagonale

  res=0
  for k in range(0,3):
    if M[k][2-k]==j:
        res=res+1
  return res


def maxi (T): #Donne le max d'une matrice 3*3

    res=T[0][0]
    for i in range(0,3):
        for j in range(0,3):
            if T[i][j]>res:
                res=T[i][j]
    return res

def occ (T,m): # Donne toutes les coordonnées d'occurrences de m dans T dans un tableau
    res=[]
    for i in range(0,3):
        for j in range(0,3):
            if T[i][j]==m:
                res=res+[(i,j)]
    return res




def evalu (): #Voici la fonction d'évaluation ! A chaque case jouable on associe un score dans une matrice, et l'IA
             # choisit la case qui a le plus de valeur. En cas d'égalité, sauf si l'IA peut gagner, c'est du random.
             # A chaque case, on associe le score (nb de 1 dans sa ligne - nb de 2 dans sa ligne)^2
             # + ( la même pour les colonnes )^2  +(la même pour les éventuelles diagonales)^2


  N= [[0,0,0],[0,0,0],[0,0,0]]


  for i in range (0,3):
    for j in range (0,3):
        if not(est_vide(i,j)): # Si on ne peut pas jouer, on affectue une valeur négative qui ne sera jamais jouée
            N[i][j]=(-1)
        else: #Il y a toujours des lignes et des colonnes pour toute case
            N[i][j]=(combien_ligne(1,i)-combien_ligne(2,i))**2 + (combien_col(1,j)-combien_col(2,j))**2
            if i==j: #On regarde les éventuelles diagonales.
               N[i][j]=N[i][j]+(combien_diag1(1)-combien_diag1(2))**2
            if (2-i)==j:
                N[i][j]=N[i][j]+(combien_diag2(1)-combien_diag2(2))**2

  m=maxi (N)  #On regarde le maximum de la fonction d'évaluation
  T=occ(N,m) #On note les ccordonnées de toutes les occurrences de ce maximum
  if score1>(score2+1):  #Si le joueur s'en sort bien, alors on corse la difficulté :)
    if T==[(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]: # Dans le cas ou le premier coup est
                                          # au centre, il faut jouer dans un coin sinon l'IA est assurée de perdre
      T=[(0, 0), (0, 2), (2, 0), (2, 2)]
  k=randrange(0,len(T))  #On choisit au hasard une de ces possibilité. S'il y en a qu'une, on ne prend que celle la !
  return T[k]


#Fin de la fonction d'évaluation





def unjoueur ():  # Dans le menu, c'est le choix de 1 vs CPU. Donc on adapte
    global fen2,cadre,fen,A,score1,score2,M
    score1=0  # On remet les scores à 0
    score2=0
    A=1  # Garde en mémoire le nombre de joueurs
    M=[[0,0,0],[0,0,0],[0,0,0]] # On reset la matrice
    jeu()  #On met en place le plateau de jeu
    cadre.bind("<Button-1>", pointeur1) # On choisir la bonne fonction pointeur
    fen2.destroy()  #On détruit cette fenêtre
    if Joueur==2: #Si c'est au CPU de jouer, bah on le fait jouer
        ordi()

    fen.mainloop()

def deuxjoueurs (): #Cas deux joueurs choisi
    global fen2,cadre,fen,Joueur,A,score1,score2,M
    score1=0  #Reset des scores
    score2=0
    M=[[0,0,0],[0,0,0],[0,0,0]] # Reset de la matrice
    A=2  # Garde en mémoire le nombre de joueurs
    jeu ()  # Mise en place du plateau de jeu
    cadre.bind("<Button-1>", pointeur2) # Choix du pointeur adéquat
    fen2.destroy ()  #Destruction de cette boite de dialogue

    fen.mainloop()




#Programme principal

def jeu ():   #Définit le plateau de jeu, après le menu principal
  global fen, cadre, bq, bm, br, hist, aqui, scor1, scor2
  fen = Tk()
  fen.title("Jeu du Morpion")
  cadre = Canvas(fen, width =300, height =300, bg="Ivory")  #Cadre de dessin
  cadre.grid(row=0,column=0,rowspan=3,columnspan=2)
  bm=Button(fen,text="Menu", command = menu)  #Bouton Menu, revient au premier menu
  bm.grid(row=0,column=2)
  br=Button(fen, text="Restart", command= restart) #Permet de recommencer une partie
  br.grid(row=1,column=2)
  bq=Button(fen, text="Quit", command= fen.destroy) #Bouton quit
  bq.grid(row=2,column=2)
  hist=Label(fen, text="La partie vient de commencer !") #Historique
  hist.grid(row=3,column=0,columnspan=2)
  aqui=Label(fen, text="Au tour du Joueur "+str(Joueur)) #Désigne à qui est le tour
  aqui.grid(row=4,column=0,columnspan=2)
  scor1=Label(fen, text="Joueur 1 : "+str(score1) )  #Affichage des scores
  scor1.grid(row=5,column=0)
  scor2=Label(fen, text="Joueur 2 : "+str(score2) )
  scor2.grid(row=5,column=1)
  quadrillage ()   #dessin du quadrillage

def menu(): #Menu principal, fenêtre d'accueil
  global fen2
  try :
      fen.destroy()
  except:
      ()
  fen2 = Tk()
  fen2.title("Jeu du Morpion - Menu ")
  titre=Label(fen2, text="Bienvenue au jeu du Morpion ! ") #Message d'accueil
  titre.grid(row=0,column=0,columnspan=2)
  titre2=Label(fen2, text="Voulez vous jouer seul ou à deux ?")
  titre2.grid(row=1,column=0,columnspan=2)
  b1=Button(fen2, text="1 Joueur", command= unjoueur)  #Bouton de choix
  b1.grid(row=2,column=0)
  b2=Button(fen2,text="2 Joueurs ", command = deuxjoueurs)
  b2.grid(row=2,column=1)
  rq=Label(fen2,text="Indiquez-moi tout bug s'il vous plait :) Bon jeu ! ")  #Message perso
  rq.grid(row=3,column=0,columnspan=2)
  qt=Button(fen2, text="Quit", command = fen2.destroy)  #Bouton quit
  qt.grid(row=4,column=0,columnspan=2)
  text4=Label(fen2,text=" © Julien Oury--Nogues")
  text4.grid(row=5,column=0,columnspan=2)



  fen2.mainloop()



menu()  #On démarre avec le menu !

















