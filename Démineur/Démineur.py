__author__ = 'Julien'


from tkinter import *
from random import *
from tkinter.ttk import *
from tkinter import ttk


#Crée une matrice n*n remplie de 0

def make_matrix (k):
    res=list()
    for i in range(k):
        res.append([0]*k)
    return res


# additionne deux ensembles A,B de telle sorte que tout soit dans A, stocké à la même adresse
def add (A,B):
    for e in B:
        A.add(e)





#Dit sur quelle case de la matrice on a cliqué
def case (x,y):
    return(x//30,y//30)



#Fonction qui place 40 mines

def place_mines ():
    global M
    M=make_matrix(nb)
    i=randrange(nb)
    j=randrange(nb)
    restant=nbmines
    while restant!=0:
        if M[i][j]!=0:
            i=randrange(nb)
            j=randrange(nb)
        else:
            M[i][j]=(-1)
            restant=restant-1
            i=randrange(nb)
            j=randrange(nb)



#Fonction qui dessine le quadrillage
def quadrillage(can):
        for i in range(0,nb*30+1,30):
            can.create_line(i,0,i,900,fill="black")
            can.create_line(0,i,900,i,fill="black")


#Ces fonctions sont vouées à  remplir la matrice initialement, comme au démineur

def est_mine (i,j):
    if M[i][j]==(-1):
        return 1
    else:
        return 0

def purge (l): #Enlève les mauvais tuples de la liste des voisins (out of range)
    res=[]
    for e in l:
        (i,j)=e
        if i!=(-1) and i!=nb and j!=-1 and j!=nb:
            res.append(e)
    return res

# Donne les vrais voisins de la case (i,j)

def voisins (i,j):
    #Fait la liste des voisins de (i,j)
    V=[(i+1,j-1),(i+1,j),(i+1,j+1),(i,j-1),(i,j+1),(i-1,j-1),(i-1,j),(i-1,j+1)]
    V=purge(V)
    return V


#Compte les Mines voisines de la case i,j
def compte_mines (i,j):
    res=0
    V=voisins(i,j)
    for e in V:
        (ii,jj)=e
        res=res+est_mine(ii,jj)
    return res

# Assigne à chaque case de M le nombre de mines qui lui sont voisines

def remplit_matrice ():
    for i in range(nb):
        for j in range(nb):
            if M[i][j]!=(-1): #Je remplis si pas de mines
                M[i][j]=compte_mines(i,j)



# Fonction qui gère les clics gauches de l'utilisateur


# je définis cette variable pour éviter de mourir dès le premier clic par malchance.


premier_clic = True


def retourne_case (event):
    global premier_clic
    (i,j)=case(event.x,event.y) # Je collecte l'information de "ou je clique"
    if premier_clic :  # Si je suis dans le premier clic
        premier_clic=False # je le désactive
        if est_mine(i,j):  #Si j'ai cliqué sur une mine
            M[i][j]=0 #j'enlève la mine
            ii=randrange(nb)
            jj=randrange(nb)
            while M[ii][jj]==(-1): #et je la mets ailleurs, pas sur une autre mine
                ii=randrange(nb)
                jj=randrange(nb)
            M[ii][jj]=-1
            remplit_matrice() #je MAJ la matrice
    if D[i][j]==1 or D[i][j]==2: #Si la case est déjà découverte ou a un drapeau dessus, je ne fais rien
        ()
    else:  # Sinon je peux opérer
        if M[i][j]==0: # dans ce cas, je découvre la case et je propage l'information, comme au vrai démineur
            decouvre_voisins(i,j)
        else:
            D[i][j]=1  # Sinon je l'affiche
            dessine_chiffre(i,j)
        if est_mine(i,j):  # Si on découvre une mine, on perd
            retourne_mines()
            perdu(i,j)
        if est_victoire(): #A chaque fois, je vérifie la condition de victoire.
            retourne_mines()
            victoire()


#Fonction qui découvre la case i,j et gère la propagation.
# Je dois me débrouiller pour ne dessine qu'une seule fois sur une case, sinon ca fait un truc moche

def decouvre_voisins (i,j):
# récupère tous les zéros qui se touchent à partir de i,j et la frontière.
    V=set(voisins(i,j)) #je récupère ses voisins
    V.add((i,j)) # je dois ajouter (i,j) dans cet algo, pour être sur qu'il soit dessiné
    res=set(V)
    for e in V:
        (ii,jj)=e
        if M[ii][jj]==0: # Si dans les voisins de i,j il y a un 0,je récupère ses voisins et je els ajoute
            add (res,voisins(ii,jj))
    while res!=V:  # je procède à cela tant que le processus me donne de nouveaux points
        V=set(res)
        for e in V:
            (ii,jj)=e
            if M[ii][jj]==0: # Si dans les voisins de i,j il y a un 0, je l'ajoute dans V !
                add(res,voisins(ii,jj))
    decouvre_tout(res)

def decouvre_tout(l):
    for e in l:
        (i,j)=e
        if D[i][j]==0: # Si il y a un drapeau, ou est déjà retourné, je ne fais rien.
            D[i][j]=1
            dessine_chiffre(i,j)





# Fonction qui place le drapeau, ou l'enlève, gèrel le clic droit




def change_drapeau(event):
    global Minesrestantes,Mines
    (i,j)=case(event.x,event.y)
    if D[i][j]==1: # Je fais rien si la case a été découverte
        ()
    else:
        D[i][j]=2-D[i][j]
        if D[i][j]==2:
            Minesrestantes=Minesrestantes-1
            dessine_drapeau(i,j)
        else:
            Minesrestantes=Minesrestantes+1
            supprime_drapeau(i,j)
    Mines.destroy()
    Mines=Label(fen1,text="Selon vous, il reste "+str(Minesrestantes)+" mine(s) ")
    Mines.grid(row=3,column=0)

# DESSINS


def dessine_drapeau(i,j):  # Fonction qui dessine le drapeau ) la case i,j
    can1.create_line(i*30+8,j*30+24,i*30+22,j*30+24,fill="black") # création du pied
    can1.create_line(i*30+15,j*30+24,i*30+15,j*30+6,fill="black") # Creation du poteau
    can1.create_polygon(i*30+15,j*30+16,i*30+15,j*30+6,i*30+5,j*30+11,fill="red",outline="black") # Et le tissu

def supprime_drapeau(i,j): # Fonction qui enlève le drapeau
    can1.create_rectangle(i*30,j*30,(i+1)*30,(j+1)*30,fill="ivory",outline="black")

# Fonction qui dessine le bon chiffre a la place i,j

def dessine_chiffre (i,j):
    chiffre=M[i][j]
    if chiffre==(-1):
        ()
    else:
        couls=["black","blue","dark green","red","dark blue","maroon","purple","yellow","dark grey"]
        can1.create_text(i*30+15,j*30+15, fill=couls[chiffre], text=str(chiffre))



# Fonction qui dessine une mine à la case i,j


def dessine_mine (i,j):
    r=7 # Je dessine un cercle de rayon 7
    can1.create_oval(i*30+15-r,j*30+15-r,i*30+15+r,j*30+15+r,fill= "black", outline="black")
    #et les branches de la mine
    can1.create_line(i*30+15,j*30+5,i*30+15,j*30+25,fill="black")
    can1.create_line(i*30+5,j*30+15,i*30+25,j*30+15,fill="black")
    can1.create_line(i*30+5,j*30+5,i*30+25,j*30+25,fill="black")
    can1.create_line(i*30+25,j*30+5,i*30+5,j*30+25,fill="black")

def dessine_croix (i,j): # Dessine une croix au centre de la case i j
       can1.create_line(30*i,30*j,30*(i+1),30*(j+1), fill="red")
       can1.create_line(30*i,30*(j+1),30*(i+1),30*j, fill="red")


# En fin de partie, je retourne toutes les mines, en fait je dévoile la solution !


def retourne_mines():
    Mines.destroy() # on enlève le compteur à drapeaux
    for i in range(nb):
        for j in range(nb):
            if M[i][j]==(-1):
                if D[i][j]!=2: # Si je n'ai pas dessiné de drapeau, je la montre
                    dessine_mine(i,j)
            else:
                if D[i][j]==2: # Si j'ai mis un drapeau au mauvais endroit, je le barre !
                    dessine_croix(i,j)




# DEFAITE

# S'active en cas de défaite (découverte d'une mine)

def stop (event): # Fonction qui ne fait rien
    ()



def perdu (i,j):
    global hist
    can1.create_rectangle(i*30,j*30,(i+1)*30,(j+1)*30,fill="red",outline="black")
    dessine_mine(i,j) # je dessine la mine
    #J'enlève au joueur la possibilité de jouer
    can1.bind("<Button-1>", stop)
    can1.bind("<Button-3>", stop)
    hist=Label(fen1,text="Vous avez perdu ! :(")
    hist.grid(row=3,column=0)

# VICTOIRE

# Définit les condtions de victoire : les 40 cases non découvertes sont exactement celles des mines

def est_victoire ():
    res=[]
    for i in range(nb):
        for j in range(nb):
            if D[i][j]!=1:
                res.append((i,j))
    if len(res)!=nbmines:
        return False
    else:
        return verification(res)  # On vérifie que les couples trouvés sont bien des mines

def verification (l):
    res=True
    for e in l:
        (i,j)=e
        res=res and est_mine(i,j)
    return res


def victoire ():
    global hist
    #J'enlève au joueur la possibilité de jouer
    can1.bind("<Button-1>", stop)
    can1.bind("<Button-3>", stop)
    hist=Label(fen1,text="Vous avez gagné, félicitations ! :D ")
    hist.grid(row=3,column=0)








# définition des niveaux de difficulté

def facile ():
    global nbmines,nb,fen,Minesrestantes,quadrillage,M,D,premier_clic
    premier_clic=True
    nbmines=10  # Définit le nombre total de mines
    nb=10  # définit la taille de la matrice carrée qui représente le jeu
    M=make_matrix(nb) # Plateau de jeu, de taille nb*nb
    D=make_matrix(nb) # ce tableau contient ce qu'on a joué : 0= rien , 1= case découverte, 2= drapeau placé
    Minesrestantes=nbmines # compteur de drapeaux pour le joueur
    fen.destroy()
    start()



def intermediaire ():
    global nbmines,nb,fen,Minesrestantes,quadrillage,M,D,premier_clic
    premier_clic=True
    nbmines=40  # Définit le nombre total de mines
    nb=15  # définit la taille de la matrice carrée qui représente le jeu
    M=make_matrix(nb) # Plateau de jeu, de taille nb*nb
    D=make_matrix(nb) # ce tableau contient ce qu'on a joué : 0= rien , 1= case découverte, 2= drapeau placé
    Minesrestantes=nbmines # compteur de drapeaux pour le joueur
    fen.destroy()
    start()

def difficile ():
    global nbmines,nb,fen,Minesrestantes,quadrillage,M,D,premier_clic
    premier_clic=True
    nbmines=100  # Définit le nombre total de mines
    nb=20  # définit la taille de la matrice carrée qui représente le jeu
    M=make_matrix(nb) # Plateau de jeu, de taille nb*nb
    D=make_matrix(nb) # ce tableau contient ce qu'on a joué : 0= rien , 1= case découverte, 2= drapeau placé
    Minesrestantes=nbmines # compteur de drapeaux pour le joueur
    fen.destroy()
    start()

# Choix personnalisé !!


def personnalise() :
    global fen2,liste
    fen.destroy()
    fen2 = Tk()
    fen2.title("Mode personnalisé")
    text=Label(fen2,text="Choisissez la taille de votre champ : ")
    text.pack()
    frame = Frame(fen2,width=300,height=300)
    frame.pack(side=TOP)
    liste = Listbox(frame) # je crée ma liste
    sbar = Scrollbar(frame) # Ma scrollbar
    sbar.config(command=liste.yview)
    liste.config(yscrollcommand=sbar.set)
    sbar.pack(side=RIGHT, fill=Y)
    liste.pack(side=LEFT, expand=YES, fill=BOTH)
    Button(fen2, text='OK', command=choix2).pack(side=BOTTOM)
    for index in range(10,21):  # j'insère dans ma liste les différents choix
        liste.insert(index,str(index)+" X "+ str(index) )

    fen2.mainloop()

def choix2():
    global nb,fen2,liste,frame
    A=(liste.get(ACTIVE))  # on récupère le choix de l'utilisateur
    (a,b)=A.split("X")
    nb= int(a)  # on définit ainsi la taille du champ.
    fen2.destroy() # je détruis l'ancienne fenêtre
    #Proposition du nombre de mines
    fen2 = Tk()
    fen2.title("Mode personnalisé")
    text=Label(fen2,text="Choisissez le nombre de mines : ")
    text.pack()
    text2=Label(fen2,text="(Nombre limité à la moitié du champ) ")
    text2.pack()
    frame = Frame(fen2)
    frame.pack(side=TOP)
    liste = Listbox(frame) # je crée ma liste
    sbar = Scrollbar(frame) # Ma scrollbar
    sbar.config(command=liste.yview)
    liste.config(yscrollcommand=sbar.set)
    sbar.pack(side=RIGHT, fill=Y)
    liste.pack(side=LEFT, expand=YES, fill=BOTH)
    Button(fen2, text='OK', command=choix3).pack(side=BOTTOM)
    for index in range(10,int((nb*nb)/2)):  # j'insère dans ma liste les différents choix
        #Je limite le nombre de mines à int((nb*nb)/2) soit la moitié du champ
        liste.insert(index, str(index) )

    fen2.mainloop()

def choix3 ():
    global nbmines,nb,fen,Minesrestantes,quadrillage,M,D,premier_clic,liste
    nbmines=int(liste.get(ACTIVE))  # je récupère la donnée de l'utilisateur
    fen2.destroy()
    premier_clic=True
    M=make_matrix(nb) # Plateau de jeu, de taille nb*nb
    D=make_matrix(nb) # ce tableau contient ce qu'on a joué : 0= rien , 1= case découverte, 2= drapeau placé
    Minesrestantes=nbmines # compteur de drapeaux pour le joueur
    start()








# Programme principal
def start ():
    global fen1,can1,Mines,b1,b2,bm
    fen1=Tk()
    fen1.title("Démineur by Julien")
    can1= Canvas(fen1, width=nb*30-4, height=nb*30-4, bg="ivory")
    # je retire 4 pixels sinon ca peut planter en cliquant aux bords
    can1.grid(row=0,column=0,rowspan=3)
    can1.bind("<Button-1>", retourne_case) #clic gauche
    can1.bind("<Button-3>", change_drapeau) # clic droit
    b2=Button(fen1,text="Recommencer",command=relance)
    b2.grid(row=0,column=1)
    bm=Button(fen1, text="Menu", command = menu2)
    bm.grid(row=1,column=1)
    b1=Button(fen1, text="Quit", command = fen1.destroy)
    b1.grid(row=2,column=1)
    Mines=Label(fen1,text="Selon vous, il reste "+str(Minesrestantes)+" mine(s)")
    Mines.grid(row=3,column=0)
    quadrillage(can1)
    place_mines()
    remplit_matrice()
    fen1.mainloop()

#Fonction qui redémarre sans changer de fenêtre, afin que ca reste propre à l'oeil


def relance ():  #  Un restart, nécessaire pour réinitialiser les variables
    global D,Minesrestantes,premier_clic,can1,Mines,b1,b2,bm
    #Réinitialisation des variables
    premier_clic=True
    Minesrestantes=nbmines  # je reinitialise ce compteur de drapeaux
    D=make_matrix(nb)  # je reinitialise D, je sais que M est de toute façon redéfini
    #Réinitialisation de la fenêtre graphique
    can1.destroy()   # je détruis tout sauf la fenêtre, afin d'éviter les pop-ups
    Mines.destroy()
    b1.destroy()
    b2.destroy()
    bm.destroy()
    try:  #essaie de détruire la feneêtre d'historique, si elle existe, sinon tu fais rien !
        hist.destroy()
    except:
        ()

    can1= Canvas(fen1, width=nb*30-4, height=nb*30-4, bg="ivory")
    # je retire 4 pixels sinon ca peut planter en cliquant aux bords
    can1.grid(row=0,column=0,rowspan=3)
    can1.bind("<Button-1>", retourne_case) #clic gauche
    can1.bind("<Button-3>", change_drapeau) # clic droit
    b2=Button(fen1,text="Recommencer",command=relance)
    b2.grid(row=0,column=1)
    bm=Button(fen1, text="Menu", command = menu2)
    bm.grid(row=1,column=1)
    b1=Button(fen1, text="Quit", command = fen1.destroy)
    b1.grid(row=2,column=1)
    Mines=Label(fen1,text="Selon vous, il reste "+str(Minesrestantes)+" mine(s)")
    Mines.grid(row=3,column=0)
    quadrillage(can1)
    place_mines()
    remplit_matrice()
    fen1.mainloop()





# Gestion du menu principal et de la difficulté !

def menu2():
    fen1.destroy()
    menu()


def menu():
    global fen
    fen=Tk()
    fen.title("Bienvenue au Démineur ! ")
    text=Label(fen,text="Bienvenue au jeu du Démineur ! :) ")
    text.grid(row=0,column=0,columnspan=2)
    text2=Label(fen,text="Choisissez votre niveau de difficulté : ")
    text2.grid(row=1,column=0,columnspan=2)
    b1=ttk.Button(fen, text="Facile", command = facile)
    b1.grid(row=2,column=0)
    b2=Button(fen, text="Intermédiaire", command = intermediaire)
    b2.grid(row=2,column=1)
    b3=Button(fen, text="Difficile", command = difficile)
    b3.grid(row=3,column=0)
    b4=Button(fen, text="Personnalisé", command = personnalise)
    b4.grid(row=3,column=1)
    text3=Label(fen,text="Bon jeu, et signalez-moi toutes vos remarques et éventuels bugs ;) ")
    text3.grid(row=4,column=0,columnspan=2)
    bq=Button(fen, text="Quit", command = fen.destroy)
    bq.grid(row=5,column=0,columnspan=2)
    text4=Label(fen,text=" © Julien Oury--Nogues")
    text4.grid(row=6,column=0,columnspan=2)
    fen.mainloop()


menu()  # lancement final du jeu !!