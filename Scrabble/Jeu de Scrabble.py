__author__ = 'Julien'

from tkinter import *
import random
from tkinter.ttk import *
from tkinter import ttk


#Crée une matrice n*n remplie de 0

def make_matrix (k):
    res=list()
    for i in range(k):
        res.append([""]*k)
    return res

#enlève les éléments de l à L. Change l'adresse

def prive (L,l):
    res=[]
    for e in L:
        if not(e in l):
            res.append(e)
    return res

#renvoie true si l est inclus dans L

def inclus (l,L):
    res=True
    for e in l:
        if not e in L:
            res=False
    return res




#Enlèves les doublons d'une liste.

def liste_purge (l):
    res=[]
    for i in range(0,len(l)):
        if not l[i] in l[(i+1):]:
            res=res+[l[i]]
    return res




#Prend en entrée une lettre minuscule, et la renvoie majuscule.
#Si la lettre est déjà en majuscule, on la laisse.

def majmin (e):
    if e in verif:   #Si c'est une minuscule
        return chr(ord(e)-32)  #On la passe en maj
    if e=="ll": #lettres espagnoles
        return "LL"
    if e=="rr":
        return "RR"
    if e=="ch":
        return "CH"
    else:   #Sinon c'est une maj
        return e

def majminmot (m):
    res=""
    try: # Si on a en entrée un truc normal
       m=convert([m])[0]
    except: #Sinon c'est que c'est un string
        ()
    for e in m:
        res=res+majmin(e)
    return res


def tassegauche ():
    global tirageJ,tempo
    res=[]
    for e in tirageJ:
        if e!="":
            res.append(e)
    k=len(res)
    tirageJ=res+[""]*(7-k)
    if k!=7:
        for e in tempo:
            if e in Regle:
                tempo.remove(e)
        for i in range(0,6):
            if tirageJ[i]!="":
                tempo.append((i+4,16))





#Fonction réciproque a la précédente

def minmaj (e):
    if e in alphabetsansaccent:   #Si c'est une majuscule
        return chr(ord(e)+32)  #On la passe en min
    if e=="CH":
        return "ch"
    if e=="LL":
        return "ll"
    if e=="RR":
        return "rr"
    else:   #Sinon c'est une minuscule
        return e

def minmajmot (m):
    res=""
    m=convert([m])[0]
    for e in m:
        res=res+minmaj(e)
    return res



M=make_matrix(15)

tirageJ=["","","","","","",""]
tirageO=["","","","","","",""]

ScoreJ=0
ScoreO=0


def est_vide(i,j):
    global tirageJ
    if (i,j)in tout_plateau: #Soit on est sur le plateau
        return (M[i][j]=="")
    elif j==16 and i>=4 and i<=10: #Soit dans la réglette
        return tirageJ[i-4]==""
    else:  #Sinon on clique n'improte ou, donc on ne peut rien faire quand meme
        return False


#Donne la liste de toutes les cases du plateau

def toutindice ():
    res=list()
    for i in range(0,15):
        for j in range(0,15):
            res.append((i,j))
    return res

tout_plateau= toutindice ()



#============================== construction du plateau de jeu


#Voici une fonction qui colorie la case (i,j) en une couleur donnée

def colorie(i,j,color):
    can.create_rectangle(i*40,j*40,(i+1)*40,(j+1)*40,fill=color,outline="black")

def trouve_color(i,j):  #Indique la couleur associée à la case
    global Blue,Red,Dblue,Pink
    if (i,j) in Blue:
        return "cyan"
    if (i,j) in Red:
        return "red"
    if (i,j) in Dblue:
        return "blue"
    if (i,j) in Pink:
        return "pink"
    if (i,j)in Regle:
        return "grey"
    else:
        return "ivory"

#Liste des cases colorées

Blue=[(0,3),(0,11),(2,6),(2,8),(3,0),(3,7),(3,14),(6,2),(6,6),(6,8),(6,12),(7,3),(7,11),(8,2),(8,6),(8,8),(8,12),(11,0),(11,7),(11,14),(12,6),(12,8),(14,3),(14,11)]
Dblue=[(1,5),(1,9),(5,1),(5,5),(5,9),(5,13),(9,1),(9,5),(9,9),(9,13),(13,5),(13,9)]
Red=[(0,0),(0,7),(0,14),(7,0),(7,14),(14,0),(14,7),(14,14)]
Pink=[(1,1),(2,2),(3,3),(4,4),(7,7),(10,10),(11,11),(12,12),(13,13),(1,13),(2,12),(3,11),(4,10),(10,4),(11,3),(12,2),(13,1)]
Regle=[(4,16),(5,16),(6,16),(7,16),(8,16),(9,16),(10,16)]

#fabrique la réglette de jeu
def reglette():
    colorie(4,16,"grey")
    colorie(5,16,"grey")
    colorie(6,16,"grey")
    colorie(7,16,"grey")
    colorie(8,16,"grey")
    colorie(9,16,"grey")
    colorie(10,16,"grey")


#je dessine le plateau, ainsi que la réglette de jeu

def plateau ():
    for i in range(0,601,40):
        can.create_line(i,0,i,600,fill="black")
        can.create_line(0,i,600,i,fill="black")
    for i in range(0,15):
        for j in range(0,15):
            can.create_rectangle(i*40,j*40,(i+1)*40,(j+1)*40,fill=trouve_color(i,j),outline="black")
    reglette()




def actualiseaffichage ():
    global M
    for i in range(0,15):
        for j in range(0,15):
            if (M[i][j] in verif) :  #Si la case sélectionnée est une minuscule
                can.create_rectangle(i*40,j*40,(i+1)*40,(j+1)*40,fill=trouve_color(i,j),outline="black")
                can.create_text(i*40+20,j*40+20,text=M[i][j])
                if M[i][j]!="":
                    can.create_text(i*40+30,j*40+30,text=pts[M[i][j]])




#=============================  tirage

# Definition des probas de tirage de chaque lettre selon le Scrabble Français
#Ordre alphabétique, Joker à la fin

#définition d'un tirage aléatoire selon le Scrabble

alphabetsansaccent= ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","?")

#Tire aléatoirement un élément dans une liste

def random_el (l):
    i=random.randrange(0, len(l))
    return l[i]

#donne toutes les lettres du jeu de Scrabble Français, le "sac"

def toutes_lettres (A):
    res=list()
    for e in A:
        (l,p)=e
        while p!=0:
            p=p-1
            res=res + [l]
    return res



def tirage_aléa (n):
    global sac
    N=len(sac)
    res=list()
    if n>N:  #S'il ne reste pas assez de lettres dans le sac, je pioche tout
        n=N
    while n!=0 :  #Je m'arrete quand quand mon compteur est terminé
         e=random_el(sac)
         n=n-1
         sac.remove(e) #Tirage sans remise
         res=res+[e]

    return res


#Programme qui affiche le tirage dans la réglette


#Cette liste retient les coordonnées des lettres temporaires avant éventuelle validation.

tempo=[]


#Affiche le tirage dans la réglette dans le canvas
def affiche():
    global tirageJ
    reglette() #On efface tout et on réaffiche
    i=4
    j=16
    for e in tirageJ:
        if e!="":
            can.create_text(i*40+20,j*40+20,text=e)
            can.create_text(i*40+30,j*40+30,text=pts[e])
        i=i+1

#Fonction qui pioche jusqu'à avoir 7 lettres dans la réglette joueur
def tireJ():
    global M,tempo,sac,tirageJ
    for i in range(0,7):
        if tirageJ[i]=="":
            l=tirage_aléa(1)
            if l!=[]:
                [e]=l
                tirageJ[i]=e
    i=4
    tempo=[]
    for e in tirageJ:  # On dit à notre fonction quelles lettres on peut cliquer...
        if e!="":
            tempo.append((i,16))
        i=i+1
    tassegauche()
    affiche()

def tireO ():
    global sac,tirageO
    for i in range(0,7):
        if tirageO[i]=="":
            l=tirage_aléa(1)
            if l!=[]:
                [e]=l
                tirageO[i]=e




#Je propose un bouton qui mélange les lettres, ce qui a pour effet de les rappeler toutes.

def melange ():
    global tirageJ
    cancel()
    rappelle()
    res=list(tirageJ)
    n=len(tirageJ)
    for i in range(0,n):
         e=random_el(res)
         tirageJ[i]=e
         res.remove(e)
    tassegauche()
    affiche()

# Je propose un bouton qui rappelle toutes les lettres

def rappelle2 ():
    global tirageJ,tempo
    for e in tempo:
        (i,j)=e
        if not (i,j) in Regle:
            lettre=M[i][j]
            if lettre in verif: #Je regarde si la lettre est une minuscule. Si c'est le cas, je la remets "?"
                lettre="?"
            M[i][j]=""
            ireplace=premier_non_vide()
            tirageJ[ireplace]=lettre
            can.create_text((ireplace+4)*40+20,16*40+20,text=lettre)
            can.create_text(i*40+30,j*40+30,text=pts[lettre])
            tempo.append((ireplace+4,16))
            tempo.remove((i,j))
            can.create_rectangle(i*40,j*40,(i+1)*40,(j+1)*40,fill=trouve_color(i,j),outline="black")
            #On termine par un redessin de la case, sinon ca reste affiché
    cancel()
    tassegauche()


#Pour une raison inconnue, il faut le faire entre 1 à 3 fois, bah bourrinons.

def rappelle ():
    for i in range(0,3):
        rappelle2()
    affiche()  #evite un bug d'affichage


#======================== Actions de remises de lettres !

#Variable globale qui dit si une fenêtre est ouverte ou non, et me dit quelle fenêtre est ouverte

fenouverte=(False,"")

#Voici la fonction qui vérifie le problème. Si l'utilisateur a bien fermé la fenetre avec une croix,
# alors il n'a pas réactivé les boutons, mais aussi fen ouverte, qui a mémorisé la dernière fenetre
# On demande alors d'effacer la console
#Si ca marche, OK on fait rien, c'ets que la fenêtre est reellement ouverte.
#Sinon, la fenêtre est fermée et il faut reactiver tous les boutons !

def testbugcroix ():
    global fenouverte,fene1,ftout,fenj,fp,fenl,fquit
    (bool,str)=fenouverte
    reactive()
    if bool:
        if str=="fene1":
            try:
                fene1.destroy()
            except:
                ()
        elif str=="ftout":
            try:
                ftout.destroy()
            except:
                ()
        elif str=="fenj":
            try:
                fenj.destroy()
            except:
                ()
        elif str=="fp":
            try:
                fp.destroy()
            except:
                ()
        elif str=="fnew":
            try:
                fnew.destroy()
            except:
                ()
        elif str=="fmenu":
            try:
                fmenu.destroy()
            except:
                ()
        elif str=="fenl":
            try:
                fenl.destroy()
            except:
                ()
        elif str=="fquit":
            try:
                fquit.destroy()
            except:
                ()

#Faisons le trois fois de suite pour être sur que ca marche !

def bourrin ():
    testbugcroix()
    testbugcroix()
    testbugcroix()

#ferme toutes les fenetres éventuellement ouvertes

def ferme_tout ():
    global fenouverte,fene1,ftout,fenj,fp,fenl,fquit
    try:
        fene1.destroy()
    except:
        ()
    try:
        ftout.destroy()
    except:
        ()
    try:
        fenj.destroy()
    except:
        ()
    try:
        fp.destroy()
    except:
        ()
    try:
        fnew.destroy()
    except:
        ()
    try:
        fmenu.destroy()
    except:
        ()
    try:
        fenl.destroy()
    except:
        ()
    try:
        fquit.destroy()
    except:
        ()




#Attention, ces deux actions font passer un tour !
#Je propose la fonction d'échanger une lettre dans le sac, ainsi que de virer la réglette
#Fonction qui prend en argument une lettre de tirageJ, la remplace, et passe son tour




def rendunelettre (e):
    global tirageJ,sac
    enleve(tirageJ,e) #on vire la lettre du tirage
    sac.append(e)  #on la remet dans le sac
    tireJ() #on retire une lettre !
    affiche()
    #METTRE UNE FONCTION "PASSE TON TOUR"

def enleve (l,e):
    for i in range(0,len(l)):
        if l[i]==e:
            l[i]=""
            break
    return l

# Voila pour rend réglette !

def rend_reglette ():
    global tirageJ,sac
    ftoutquit()
    for e in tirageJ:
        if e!="":  #Si le machin est pas vide, on le vire
            tirageJ=enleve (tirageJ,e) #on vire la lettre du tirage
            sac.append(e)  #on la remet dans le sac
    tireJ()
    affiche()
    passeJ()


def echangetout ():
    global tirageJ,sac,ftout,fenouverte
    fenouverte=(True,"ftout")
    suspend()
    cancel()
    rappelle()
    ferme_tout()
    ftout=Tk()
    ftout.title("Êtes-vous sûr ?")
    text=Label(ftout,text="Êtes-vous sûr de vouloir échanger votre réglette ?")
    text.grid(row=0,column=0,columnspan=2)
    text2=Label(ftout,text="Vous passerez alors votre tour")
    text2.grid(row=1,column=0,columnspan=2)
    by=Button(ftout,text="Oui",command=rend_reglette)
    by.grid(row=2,column=0)
    bn=Button(ftout,text="Non",command=ftoutquit)
    bn.grid(row=2,column=1)

def ftoutquit ():
    global ftout
    reactive()
    ftout.destroy()



#Concernant l'échange d'une seule lettre

def echange1 ():
    global fene1,entreech,fenouverte
    fenouverte=(True,"fene1")
    suspend()
    cancel()
    rappelle()
    ferme_tout()
    fene1=Tk()
    fene1.title("Choix de la lettre à supprimer")
    text=Label(fene1,text="Veuillez entrez en lettre minuscule la lettre que vous voulez échanger")
    text.pack()
    textb=Label(fene1,text="Attention, cela vous obligera à passer votre tour")
    textb.pack()
    entreech = Entry(fene1)
    entreech.bind("<Return>", echanger1)
    entreech.pack()
    text2=Label(fene1,text="Et appuyez sur la touche Entrée")
    text2.pack()
    bqf=Button(fene1,text="Quit",command=fene1quit)
    bqf.pack()
    fene1.mainloop()

def echanger1 (event):
    global fene1,entreech
    e=entreech.get()
    if e!="": #Si un petit malin met rien, alors on fait rien
        e=majmin(e)
        if e in tirageJ:  #Si un petit malin met n'imp, on fait rien
            reactive()
            fene1.destroy()
            rendunelettre(e)
            passeJ()

def fene1quit ():
    global fene1
    reactive()
    fene1.destroy()





#Fonction qui va gérer le jeu. On va regarder les lettres jouées, et vérifier si le mot est joué en une ligne,
#  Rechercher tous les mots joués, et vérifier s'il est dans le lexique.

#Variable globale pour rechercher les Jokers...
peutchercherJok=True

#définit la passe joueur
#Dans le cas d'un changement de lettre

def passeJ ():
    global justepasse
    effacemess()
    affichemess("Vous passez votre tour")
    justepasse=False # On a échangé une ou toutes les lettres. Ce n'est pas une passe
    actuhisto("Joueur passe")
    fen.after(100,ordi)

def passeJvoulue():
    global justepasse
    effacemess()
    affichemess("Vous passez votre tour")
    actuhisto("Joueur passe")
    if justepasse:
        matchnul()
    else:
        justepasse=True
        fen.after(100,ordi)


#définit la passe de l'ordinateur

def passeO ():
    global justepasse
    effacemess()
    affichemess("L'ordinateur passe son tour")
    actuhisto("Ordi passe")
    if justepasse:
        matchnul()
    else:
        justepasse=True

def passeconf ():
    global fenouverte,fp
    cancel()
    rappelle()
    suspend()
    ferme_tout()
    fenouverte=(True,"fp")
    fp=Tk()
    fp.title("Confirmation")
    text=Label(fp,text="Souhaitez vous rééllement passer votre tour ?")
    text.grid(row=0,column=0,columnspan=2)
    by=Button(fp,text="Oui",command=passejoueur)
    by.grid(row=1,column=0)
    bn=Button(fp,text="Non",command=fpassquit)
    bn.grid(row=1,column=1)

def passejoueur():
    fpassquit()
    passeJvoulue()

def fpassquit ():
    global fenouverte,fp
    fenouverte=(False,"")
    fp.destroy()
    reactive()



def jeu ():
    global tempo,Regle,premier_coup,valeursJoks,peutchercherJok,enmain,tirageJ,justepasse
    lettres_jouees=prive(tempo,Regle)
    if peutchercherJok:  #Se fait en deux temps. Je lance la recherche de Jokers. Je la désactive car je rappelle jeu()
                         #Puis je réactive une éventuelle recherche.
        (nbj,coords)=cherchejoker(lettres_jouees)
        fenjok(nbj,coords)
        peutchercherJok=False
    if premier_coup:
        premier_coup=False
        cancel()  #Pour éviter les bugs, on réinitialise :)
        peutchercherJok=True
        tireJ()
        tireO()
    elif lettres_jouees==[]:
        cancel()  #Pour éviter les bugs, on réinitialise :)
        peutchercherJok=True
        affichemess("Vous devez jouez un mot avant de valider ! ")
    else:
        (surligne,type)=tout_uneligne(lettres_jouees) # On vérifie que toutes les lettres sont sur une meme ligne/col
        if surligne:
            if type =="ligne":
                lettres_jouees=triligne(lettres_jouees) #On vérifie qu'il n'y a pas de trous
                pastrou=estpleinL(lettres_jouees)
                vois=regle_voisins(lettres_jouees) # On ajoute la règle des voisins
            elif type=="colonne": #On vérifie qu'il n'y a pas de trous
                lettres_jouees=tricol(lettres_jouees)
                pastrou=estpleinC(lettres_jouees)
                vois=regle_voisins(lettres_jouees) # On ajoute la règle des voisins
            if (pastrou and vois) :  # ICI ON EST DANS LE CAS DU COUP VALIDE
                #On va vérifier que tous les mots joués sont dans le dictionnaire
                toutmots=tout_mots_joues(toutvoisins(lettres_jouees),lettres_jouees)
                if coupvalable(toutmots):
                    affichecoup(scores(lettres_jouees)) #Affiche les mots joués et leur score
                    actualiseaffichage() #Remplace les éventuels ? par les lettres effectivement jouées
                    tempo=prive(tempo,lettres_jouees)   #Les lettres jouées deviennent définitives, et intouchables
                    cancel()  #Pour éviter les bugs, on réinitialise :)
                    peutchercherJok=True
                    #Il faut redessiner la case tenue par memo, car si elle est sélectionnée avant
                    # validation, la lettre disparait.
                    (i,j)=memo
                    if (i,j) in tout_plateau:
                        can.create_rectangle(i*40,j*40,(i+1)*40,(j+1)*40,fill=trouve_color(i,j),outline="black")
                        can.create_text(i*40+20,j*40+20,text=M[i][j])
                        can.create_text(i*40+30,j*40+30,text=pts[M[i][j]])
                    (bool,gagnant)=est_victoire()
                    if bool:
                        victoire(gagnant)
                    else:
                        tireJ()
                        affiche_lettres_rest()
                        justepasse=False
                        fen.after(100,ordi) # On laisse le temps à la machine d'afficher mes scores, avant de lancer ordi
                else:
                    for e in toutmots:
                        if not(motvalable(e)):
                            affichemess("Faute : le mot "+convert([e])[0]+" n'est pas dans le lexique")
                    valeursJoks=[] #J'enlève l'affectation de mes Jokers
                    peutchercherJok=True
                    rappelle()
            else: #je détaille les erreurs pour personnaliser le message d'erreur
                if not(vois):
                    if toutvoisins(lettres_jouees)==[]:
                        if M[7][7]=="":
                            affichemess("Faute : votre mot doit obligatoirement passer par la case centrale (7,7)")
                        else:
                            affichemess("Faute : votre mot doit être raccordé à d'autres mots du plateau. ")
                elif not(pastrou):
                    affichemess("Faute : votre mot doit former une ligne continue, éventuellement avec les lettres du plateau")
                cancel()  #Pour éviter les bugs, on réinitialise :)
                peutchercherJok=True
                rappelle()
        else:
            affichemess("Faute : votre mot doit être sur une même ligne ou colonne ")
            cancel()  #Pour éviter les bugs, on réinitialise :)
            peutchercherJok=True
            rappelle()



#====================== GESTION DES JOKERS


def cherchejoker (joues):
    nb=0
    coords=[]
    for e in joues:  #On compte le nombre de Joker, 0 1 ou 2 et on stocke leurs coordonnées
        (i,j)=e
        if M[i][j]=="?":
            nb=nb+1
            coords.append(e)
    return(nb,coords)

verif="abcdefghijklmnopqrstuvwxyz"


#Je dois faire deux fonctions. Une évaluer1 et évaluer2 au cas ou on a 1 ou deux jokers...

#Cas de un Joker

def evaluer1 (event):
    global a,fenj,NB,COORDS,langue
    a=entree.get()
    if langue=="ES":
        if a in list(verif)+["ch","ll","rr"]:
            reactive()
            fenj.destroy()
            e=COORDS[0]
            (i,j)=e
            M[i][j]=a
            valeursJoks.append(a)
            jeu()  #On relance le jeu tout de suite
    else:
        if a in verif:
            reactive()
            fenj.destroy()
            e=COORDS[0]
            (i,j)=e
            M[i][j]=a
            valeursJoks.append(a)
            jeu()  #On relance le jeu tout de suite

#Cas de 2 jokers

def evaluer2(event):
    global a,fenj,NB,COORDS,entree2,fenouverte,langue
    res=entree.get()
    if len(res)==3 and res[0]!=" " and res[2]!=" " and res[1]==" ":
        (a,b)=res.split()
        if (a in verif) and (b in verif):
            fenj.destroy()
            e=COORDS[0]
            (i,j)=e
            M[i][j]=a
            valeursJoks.append(a)
            reactive()
            e=COORDS[1]
            (i,j)=e
            M[i][j]=b
            valeursJoks.append(b)
            jeu()  #La on peut redonner la main.
    elif langue=="ES":  #prendre en compte les lettres doubles en espagnol.
        if len(res)==4 and res[0]!=" " and res[2]==" " and res[1]!=" " and res[3]!=" ":
            (a,b)=res.split()
            if (a in ["ch","ll","rr"]) and (b in verif):
                fenj.destroy()
                e=COORDS[0]
                (i,j)=e
                M[i][j]=a
                valeursJoks.append(a)
                reactive()
                e=COORDS[1]
                (i,j)=e
                M[i][j]=b
                valeursJoks.append(b)
                jeu()  #La on peut redonner la main.
        if len(res)==4 and res[0]!=" " and res[2]!=" " and res[1]==" " and res[3]!=" ":
            (a,b)=res.split()
            if (b in ["ch","ll","rr"]) and (a in verif):
                fenj.destroy()
                e=COORDS[0]
                (i,j)=e
                M[i][j]=a
                valeursJoks.append(a)
                reactive()
                e=COORDS[1]
                (i,j)=e
                M[i][j]=b
                valeursJoks.append(b)
                jeu()  #La on peut redonner la main.
        if len(res)==5 and res[0]!=" " and res[2]==" " and res[1]!=" " and res[3]!=" " and res[4]!=" ":
            (a,b)=res.split()
            if (b in ["ch","ll","rr"]) and (a in ["ch","ll","rr"]):
                fenj.destroy()
                e=COORDS[0]
                (i,j)=e
                M[i][j]=a
                valeursJoks.append(a)
                reactive()
                e=COORDS[1]
                (i,j)=e
                M[i][j]=b
                valeursJoks.append(b)
                jeu()  #La on peut redonner la main.


#Voici les valeurs des Jokers, on initialise

valeursJoks=[]


def fenjok (nb,coords):
    global entree,fenj,NB,COORDS,valeursJoks,fenouverte
    valeursJoks=[]
    COORDS=coords
    NB=nb
    ferme_tout()
    if nb==1:
        suspend()
        fenouverte=(True,"fenj")
        fenj=Tk()
        fenj.title("Choix de lettres pour vos Jokers")
        text=Label(fenj,text="Veuillez entrer en lettre minuscule la lettre que vous affectez à votre Joker")
        text.pack()
        entree = Entry(fenj)
        entree.bind("<Return>", evaluer1)
        entree.pack()
        text2=Label(fenj,text="Et appuyez sur la touche Entrée")
        text2.pack()
        bqj=Button(fenj,text="Quit",command=fenjquit)
        bqj.pack()
        fenj.mainloop()
    elif nb==2:  # Je change la fonction evaluer en cas de 2 Jokers
        suspend()
        fenouverte=(True,"fenj")
        fenj=Tk()
        fenj.title("Choix de lettres pour vos Jokers")
        text=Label(fenj,text="Veuillez entrer en lettres minuscules séparées d'un espace les lettres pour le premier et second joker")
        text.pack()
        entree = Entry(fenj)
        entree.bind("<Return>", evaluer2)
        entree.pack()
        text2=Label(fenj,text="Et appuyez sur la touche Entrée")
        text2.pack()
        bqj=Button(fenj,text="Quit",command=fenjquit)
        bqj.pack()
        fenj.mainloop()


def fenjquit ():
    global fenj
    reactive()
    rappelle()
    fenj.destroy()





#===============  REGLES



#Fonction qui désactive temporairement tous les boutons du plateau de jeu principal

def rien(event=0):
    if event==0:
        bourrin()

def rienrap ():
    rien()
    rappelle()


def rienq ():
    rien()
    fenquitconf()


def rienmix ():

    rien()
    melange()


def rient ():
    rien()
    jeu()

def rienlex ():
    rien()
    ouvre_lexique()


def rien1let ():
    rien()
    echange1()


def rientout ():
    rien()
    echangetout()

def rienp ():
    rien ()
    passeconf ()

def rienmenu ():
    rien()
    menuconf()

def riennew ():
    rien()
    newconf()

def suspend ():
    global can,bq,brap,bmix,bt,blex,b1let,btout,bp,bmenu,bnew
    bq.config(command=rienq)
    brap.config(command=rienrap)
    bmix.config(command=rienmix)
    bt.config(command=rient)
    blex.config(command=rienlex)
    b1let.config(command=rien1let)
    btout.config(command=rientout)
    bp.config(command=rienp)
    bmenu.config(command=rienmenu)
    bnew.config(command=riennew)
    can.bind("<Button-1>",rien)
    can.bind("<Button-3>",rien)


def suspendvrai ():
    global can,bq,brap,bmix,bt,blex,b1let,btout,bp,bmenu,bnew
    bq.config(command=rienvrai)
    brap.config(command=rienvrai)
    bmix.config(command=rienvrai)
    bt.config(command=rienvrai)
    blex.config(command=rienvrai)
    b1let.config(command=rienvrai)
    btout.config(command=rienvrai)
    bp.config(command=rienvrai)
    bmenu.config(command=rienvrai)
    bnew.config(command=rienvrai)
    can.bind("<Button-1>",rienvrai)
    can.bind("<Button-3>",rienvrai)

#Ne fait vraiment rien ^^

def rienvrai (event=0):
    ()


#Fonction qui réactive tous les boutons

def reactive ():
    global can,bq,brap,bmix,bt,blex,b1let,btout,fenouverte,bp,bmenu,bnew
    fenouverte=(False,"")
    bq.config(command=fenquitconf)
    brap.config(command=rappelle)
    bmix.config(command=melange)
    bt.config(command=jeu)
    blex.config(command=ouvre_lexique)
    b1let.config(command=echange1)
    btout.config(command=echangetout)
    bp.config(command=passeconf)
    bmenu.config(command=menuconf)
    bnew.config(command=newconf)
    can.bind("<Button-1>",select)
    can.bind("<Button-3>",cancel)



#On va vérifier si toutes les lettres jouées sont sur une même ligne ou une même colonne.

#donne les coordonnées de la colonne j

def colonne (j):
    res=[]
    for i in range(0,15):
        res.append((i,j))
    return res

#Donne les coordonnées de la ligne i

def ligne (i):
    res=[]
    for j in range(0,15):
        res.append((i,j))
    return res




def tout_uneligne (l):
    res=(False,"")
    for i in range(0,15):
        if inclus(l,ligne(i)):
            res=(True,'ligne')
            break
        elif inclus(l,colonne(i)):
            res=(True,"colonne")
            break
    return res



#Fonction qui trie une liste de (a,b) selon a pour ligne, b pour colonne.


def tricol (l):
    if l==[]:
        return l
    (a,b)=l[0]
    intermede=[] #Je vais collecter tous les a, les trier, et les remettre avec leur b, tous égal !
    for e in l:
        (i,j)=e
        intermede.append(i)
    intermede.sort()  #je trie les a
    res=[]
    for e in intermede:  #Je les remets avec les b
        res.append((e,b))
    return res


def triligne (l):
    if l==[]:
        return l
    (a,b)=l[0]
    intermede=[] #Je vais collecter tous les b, les trier, et les remettre avec leur a, tous égal !
    for e in l:
        (i,j)=e
        intermede.append(j)
    intermede.sort()  # Je trie les b
    res=[]
    for e in intermede: #je les remets avec les a
        res.append((a,e))
    return res



#Cette fonction vérifie une autre règle du scrabble, que les lettres jouées, supposées sur la même ligne ou colonne,
# doivent être jointes entre elles, et les lettres du plateau.
#Je fais deux fonctions, une pour les lignes et une pour les colonnes


def estpleinL (l):
    global M
    if l==[]:
        return True
    (a,jmin)=l[0]
    (a,jmax)=l[len(l)-1]
    res=True
    for j in range(jmin,jmax+1):
        res=res and ((a,j)in l or (M[a][j]!=""))
    return res


def estpleinC(l):
    global M
    if l==[]:
        return True
    (imin,b)=l[0]
    (imax,b)=l[len(l)-1]
    res=True
    for i in range(imin,imax+1):
        res=res and ((i,b)in l or (M[i][b]!=""))
    return res



#Cas de match nul : les joueurs passent tous les deux

def matchnul():
    global ScoreJ,ScoreO,bq,bmenu,bnew
    suspendvrai()
    enregistre()
    bq.config(command=fen.destroy)
    bnew.config(command=newconf)
    bmenu.config(command=menuconf)
    malusJ=valeur(tirageJ)
    ScoreJ=ScoreJ-malusJ
    malusO=valeur(tirageO)
    ScoreO=ScoreO-malusO
    text="Vous perdez "+str(malusJ)+" points de malus ! Votre adversaire "+str(malusO)+" points !"
    affiche_score()
    if ScoreJ>ScoreO:
        affichemess(text+" Vous avez gagné, félicitations :D !")
    if ScoreO>ScoreJ:
        affichemess(text+ " Dommage, l'ordinateur remporte la partie !")
    if ScoreO==ScoreJ:
        affichemess(text+ " Match nul ! Bien joué !")



#Définit la condition de victoire. Plus de pions dans le sac et une reglette vide !

def est_victoire ():
    if len(sac)==0:
        if tirageJ==["","","","","","",""]:
            return(True,"Joueur")
        elif tirageO==["","","","","","",""]:
            return(True,"Ordinateur")
        else:
            return(False,"")
    else:
        return(False,"")

#Effectue le décompte final des points (bonus, malus)

def valeur (l):
    res=0
    for e in l:
        if e!="":
            res=res+pts[e]
    return res

def victoire (gagnant):
    global bq,ScoreJ,ScoreO,bmenu,bnew
    affiche_lettres_rest()
    suspendvrai()
    bq.config(command=fen.destroy)
    bnew.config(command=newconf)
    bmenu.config(command=menuconf)
    if gagnant=="Joueur":
        bonus=valeur(tirageO)
        ScoreJ=ScoreJ+bonus
        ScoreO=ScoreO-bonus
        text="Vous obtenez "+str(bonus)+" points bonus !"
    elif gagnant=="Ordinateur":
        bonus=valeur(tirageJ)
        ScoreJ=ScoreJ-bonus
        ScoreO=ScoreO+bonus
        text="L'ordinateur obtient "+str(bonus)+" points bonus !"
    affiche_score()
    if ScoreJ>ScoreO:
        affichemess(text+" Vous avez gagné, félicitations :D !")
    if ScoreO>ScoreJ:
        affichemess(text+ " Dommage, l'ordinateur remporte la partie !")
    if ScoreO==ScoreJ:
        affichemess(text+ " Match nul ! Bien joué !")
    enregistre()




# Vérifions cette règle : En plaçant un mot, il doit au minimum joindre une autre lettre du plateau,
# sauf si le mot a une lettre placée en (7,7)

#Je dois donc collecter la liste des lettres voisines, étant données M et lettres jouées
# Je renverrai un résultat du type [((coords de la lettre),(coords du voisin))]


#Cette fonction donne d'abord tous les voisins non vide.

def purge (l):
    res = []
    for e in l:
        (i,j)=e
        if not(i<0 or j<0 or i>14 or j>14)  : #On évite le out of range
            if M[i][j]!="": #Puis on vérifie si les voisins sont vides ou non.
                res.append(e)
    return res

def voisins (i,j):
    return purge ([(i+1,j),(i-1,j),(i,j+1),(i,j-1)])


def toutvoisins (joues):
    res=[]
    for e in joues:
        (i,j)=e
        l=voisins(i,j)
        l=prive(l,joues)
        l=complete(i,j,l)  #Je mets le format annoncé [((coords de la lettre),(coords du voisin))]
        res=res+l
    return res

def complete (i,j,l):
    res=[]
    for e in l:
        res.append(((i,j),e))
    return res


def regle_voisins (joues):
    l=toutvoisins(joues)
    if l==[] and not (7,7) in joues: #On vérifie qu'il y a au moins un raccordement,
                                     # ou alors qu'on a joué au centre au cas d'un premier coup
        return False
    else:
        return True



#A partir de tous les voisins, je vais trouver tous les mots qui sont formés !

def tout_mots_joues (l,joues):
    global M
    res= list() #J'enlèverai les doublons par un liste purge. Un set ne marche pas !
    for e in l:
        place=e[0] #c'est la coordonnée du pion placé
        voisi=e[1] #coordonnée du voisin
        (ip,jp)=place
        (iv,jv)=voisi
        mot=[] #On va stocker les coordonnées du mot en entier
        if ip==iv: #Alors on doit chercher sur la ligne ip=iv !
            j=jp
            while j<15 and M[ip][j]!="":
                mot.append((ip,j))
                j=j+1
            j=jp-1
            while j>(-1) and M[ip][j]!="":
                mot.append((ip,j))
                j=j-1
            mot=triligne(mot) #Je trie les coordonnées de manière canonique, pour qu'on puisse le lire !
            res.append(mot)
        elif jp==jv:  #Alors on doit chercher sur la colonne jp=jv !
            i=ip
            while i<15 and M[i][jp]!="":
                mot.append((i,jp))
                i=i+1
            i=ip-1
            while i>(-1) and M[i][jp]!="":
                mot.append((i,jp))
                i=i-1
            mot=tricol(mot) #Je trie les coordonnées de manière canonique, pour qu'on puisse le lire !
            res.append(mot)
    #Il faut ajouter le mot principal sauf si il est sous mot d'un mot déjà compté

    ajout_joue=True #je l'ajoute si cette variable est True a la fin
    for e in res:
        if inclus(joues,e):
            ajout_joue=False
            break
    if ajout_joue:
        res=res+[joues]
    return liste_purge(res)


#Prend une liste de liste de coordonnées jouées, et en donne une liste de mots joués !

def convert (l):
    global M
    res=[]
    for coord in l:
        mot=""
        for e in coord:
            (i,j)=e
            mot=mot+M[i][j]
        res.append(mot)
    return res


#========= SCORE

#On va calculer le score d'un coup à partir de l "tous mots joués" et les lettres jouées.

#Cela s'afficher ainsi, mot,score associé

def scores (jouees):
    res=[]
    toutmots=tout_mots_joues(toutvoisins(jouees),jouees)
    scrabble=len(jouees)==7 #condition de Scrabble
    for mot in toutmots:
        mult=1 #multiplicateur de mots (cases roses et rouges)
        sco=0 #score total du mot
        for lettre in mot:
            (i,j)=lettre
            s=pts[M[i][j]]
            if (i,j) in jouees: #On ne compte les multiplicateurs que si on pose une lettre dessus
                if (i,j) in Blue:
                    s=2*s
                if (i,j) in Dblue:
                    s=3*s
                if (i,j) in Pink:
                    mult=2*mult
                if (i,j) in Red:
                    mult=3*mult
            sco=sco+s
        sco=sco*mult
        if scrabble: #Bonus de 50 points au Scrabble rajouté au mot d 7 lettres.
            if inclus (jouees,mot):
                sco=sco+50
        motreel=convert([mot])
        res.append((motreel,sco))
    if not(ORDI):    #Si c'est bien a moi de jouer
        motatester(res,jouees)    #Je regarde si on n'a pas à faire au meilleur mot joué !
    return res



#Je vais trouver, a partir de res, le score total, ainsi que le mot qui a été joué.

def motpluslong (l):
    res=""
    for e in l:
        if len(e)>len(res):
            res=e
    return res

def motatester (resuscores,jouees):
    global meilleurmot,meilleurscoremot
    scotot=0
    motsfinal=[]
    test=(convert([jouees]))
    test=test[0]
    for (mot,sco) in resuscores:
        scotot=scotot+sco
        mot=mot[0]
        if inclusordre(mot,test):
            motsfinal.append(mot)
    motfin=motpluslong(motsfinal)
    changemot(motfin,scotot)



#Donne l'inclusion ordonnée

def inclusordre (l,L):
    il=0
    iL=0
    while iL!=len(L) and il!=len(l):
        if l[il]==L[iL]:
            il=il+1
            iL=iL+1
        else:
            iL=iL+1
    return il==len(l)







def affiche_score():
    global ScoreJ,ScoreO
    can.create_rectangle(450,641,590,700,fill="ivory",outline="blue") #On efface
    can.create_text(520,655,text="Votre score : "+str(ScoreJ))
    can.create_text(520,685,text="Score ordinateur : "+str(ScoreO))





#================================ Gestion du lexique










#Je vais proposer un affichage du lexique dans une autre fenêtre..
#Variable globale qui indique si le lexique est déjà ouvert.
# S'il est ouvert, alors la pression sur le bouton lexique n'affichera rien de plus




#Fonction pour quitter, je remets bien à False, et je désactive

def lexquit ():
    global fenl,fenouverte
    fenouverte=(False,"")
    fenl.destroy()



def ouvre_lexique ():
    global fenl,entree3,liste,fenouverte
    try:
        fenl.destroy()
    except:
        ()
    fenouverte=(True,"fenl")
    fenl=Tk()
    fenl.title("Consultation du lexique ("+str(len(lexique))+" mots) ")
    text=Label(fenl,text="Veuillez entrer votre mot à rechercher dans le lexique")
    text.pack()
    entree3 = Entry(fenl)
    entree3.bind("<Return>", recherche)
    entree3.pack()
    text2=Label(fenl,text="Et appuyez sur la touche Entrée")
    text2.pack()
    frame = Frame(fenl)
    frame.pack(side=TOP)
    liste = Listbox(frame) # je crée ma liste
    sbar = Scrollbar(frame) # Ma scrollbar
    sbar.config(command=liste.yview)
    liste.config(yscrollcommand=sbar.set)
    sbar.pack(side=RIGHT, fill=Y)
    liste.pack(side=LEFT, expand=YES, fill=BOTH)
    Button(fenl, text='Quit', command=lexquit).pack(side=BOTTOM)
    i=0
    for e in lexique:  # j'insère dans ma liste les différents choix
        liste.insert(i,e)
        i=i+1
    fenl.mainloop()


def recherche (event):
    global entree3,liste
    mot=majminmot(entree3.get())
    i=cherche(mot,lexique)
    liste.see(i)


#Algorithme de recherche dans une liste triée

def cherche(mot,liste):
    fin=len(liste)-1
    debut=0
    while abs(debut-fin)>1 :
        k=(debut+fin)//2
        if liste[k]>=mot:
            fin=k
        else:
            debut=k
    if mot==liste[fin]:  #On retourne, fin ou l[fin] dans ce cas (vérifier, ca marche)
        return fin
    else: #On retourne l[début] ou début.
        return debut




# Maintenant, je fais une fonction qui dit si un mot est dans le lexique ou pas.
#ATTENTION : le joueur aura éventuellement affecté son ou ses Jokers avant.


def motvalable (mot):
    mot2=majminmot(mot)
    return mot2 in lexique

#Coup valable si la liste des mots jouées est dans le lexique

def coupvalable (l):
    for e in l:
        if not motvalable(e):
            return False
    return True










#============== Placement des lettres, et gestion graphique


def case (x,y):
    return(x//40,y//40)

#Dit si on a une lettre dans notre main
enmain=False

#garde en mémoire la case cliquée
memo=(16,16)


#Met un carré noir sur la case sélectionnée
def selectionne(i,j):
    can.create_rectangle(i*40,j*40,(i+1)*40,j*40+2,fill="black")
    can.create_rectangle(i*40,j*40,i*40+2,(j+1)*40,fill="black")
    can.create_rectangle(i*40,(j+1)*40-2,(i+1)*40,(j+1)*40,fill="black")
    can.create_rectangle((i+1)*40-2,j*40,(i+1)*40,(j+1)*40,fill="black")


#Enlève le contour noir
def deselect (i,j):
    can.create_rectangle(i*40,j*40,(i+1)*40,(j+1)*40,fill=trouve_color(i,j),outline="black")





# gère le clic gauche dans le canvas
#Probablement ma fonction la plus incompréhensible, mais qui marche
def select(event):
    global tempo,tirageJ,enmain,memo,M,tout_plateau
    (i,j)=case(event.x,event.y) # Je collecte l'information de "ou je clique"
    if not enmain:
        if (i,j)in tempo:
            enmain=True
            selectionne(i,j)
            memo=(i,j)
    else:
        if ((i,j) in tout_plateau or (i,j)in Regle) and est_vide(i,j)  :
            enmain=False
            (ii,jj)=memo
            deselect(ii,jj)
            lettre=""
            if memo in Regle:
                lettre=tirageJ[ii-4]
                tirageJ[ii-4]=""
            else:
                lettre=M[ii][jj]
                M[ii][jj]=""
            can.create_text(i*40+20,j*40+20,text=lettre)
            can.create_text(i*40+30,j*40+30,text=pts[lettre])
            if not((i,j) in Regle):
                M[i][j]=lettre
            else:
                tirageJ[i-4]=lettre
            tempo.append((i,j))
            tempo.remove((ii,jj))
            memo=(i,j)


#gère le clic droit, permet de rappeler une lettre dans la réglette en cliquant dessus,
# ou alors en cliquant en ayant séléctionné déjà.


def cancel (event=0):
    global memo,tempo,enmain
    try: # Si ca marche pas, c'était un cas imprévu, donc ca ne doit rien faire.
      if enmain:
        (i,j)=memo
        deselect(i,j)
        enmain=False
        if (i,j) in Regle:
            affiche()
        else:
            if (i,j) in tempo:
                lettre=M[i][j]
                M[i][j]=""
                ireplace=premier_non_vide()
                tirageJ[ireplace]=lettre
                can.create_text((ireplace+4)*40+20,16*40+20,text=lettre)
                can.create_text((ireplace+4)*40+30,16*40+30,text=pts[lettre])
                tempo.append((ireplace+4,16))
                tempo.remove((i,j))
      elif event!=0:
        (i,j)=case(event.x,event.y)
        if (i,j) in tempo:
            deselect(i,j)
        enmain=False
        if (i,j) in Regle:
            affiche()  #Equivaut à deselect, mais évite les bugs.
        else:
            if (i,j)in tempo:
                lettre=M[i][j]
                M[i][j]=""
                ireplace=premier_non_vide()
                tirageJ[ireplace]=lettre
                can.create_text((ireplace+4)*40+20,16*40+20,text=lettre)
                can.create_text((ireplace+4)*40+30,16*40+30,text=pts[lettre])
                tempo.append((ireplace+4,16))
                tempo.remove((i,j))
    except:
        ()




def premier_non_vide ():
    global tirageJ
    i=0
    while tirageJ[i]!="":
        i=i+1
    return i




#Je fais une fonction qui permet d'affihcer des messages (typiquement d'erreur) entre la réglette et le plateau


def affichemess (str):
    effacemess() #Pour éviter l'empilage débile
    can.create_text(300,15*40+20,text=str)

#efface le message entre la réglette et le plateau de jeu
def effacemess ():
    can.create_rectangle(0,15*40+10,14*40,15*40+30,fill="ivory",outline="ivory")


def affichecoup (l):
    global ScoreJ
    res="Vous avez joué : "
    tot=0
    for e in l:
        (mot,sco)=e
        tot=tot+sco
        mot=mot[0]
        res=res+mot+" (" + str(sco)+"), "
    ScoreJ=ScoreJ+tot
    effacemess()
    actuhisto("Joueur "+res[14:len(res)-2])
    affiche_score()
    can.create_text(300,15*40+20,text=res[:len(res)-2])


def nblettres(l):
    res=0
    for e in l:
        if e!="":
            res+=1
    return str(res)

def affiche_lettres_rest():
    global sac,tirageO
    can.create_rectangle(10,641,150,700,fill="ivory",outline="blue")
    can.create_text(80,655,text="Il reste "+str(len(sac))+" lettres ! ")
    can.create_text(80,685,text="Ordi a "+nblettres(tirageO)+" lettres !")



#======================= IA ======================================


#Etant donné un tirage d'ordinateur, auquel je rajoute un "?" pour augmenter sa réflexion,
#Je cherche tous les mots qui peuvent être écrits par l'ordinateur.

def tousmots (lexique,lettres):
    les_mots=list() # retourne tous les mots possibles
    for mot in lexique:
        if peut_ecrire (mot,lettres):
            les_mots.append(mot)
    return les_mots


def peut_ecrire (mot,lettres):
    global Scoremalus
    Scoremalus=0
    J=combien_joker(lettres)
    restant=list(lettres)  # Je change l'adressage, attention au mutable sinon ca plante
    res=True
    for e in mot:
        if e in restant :
          restant.remove(e)
        elif J!=0:
          J=J-1
          restant.remove("?")
        else :
          res=False
          break
    return (res)


#Dans un tirage de lettres, dit combien il y a de Jokers

def combien_joker (l):
    res=0
    for e in l:
        if e=="?":
            res=res+1
    return res


# Mon idée. On va se ballader sur le plateau avec une fenêtre de 8 qu'on déplace, horizontale puis verticale
#On regarde si on place un mot dans cet endroit on ne le place pas dans le vide, sinon on bouge
#Si on ne le place pas dans le vide, alors on teste tous les mots, on note éventuellement les mots qu'on peut jouer et
#on calcule son score.

#Faire attention aux lettres déjà placées. Si des lettres sont déjà placées, on peut s'en servir, l'ajouter au tirage
# (se servir du ? de réflexion)
#(le retirer juste après). Si plus de 2 lettres sont collées ou sont dans le tirage rajoutées,
#  on décrète qu'il est impossible de jouer ici et on passe

# On renverra : les lettres jouées associées a leur placement. ce tuple de deux on associera le score une liste de :
# (((lettre1,placementdelalettre1),(lettre2,placement2),...,(lettrefin,placementfin)),score du mot)

#Dans l'IA, faire un cas au cas ou c'est elle qui commence (cas M vide), c'est à dire, si c'ets elle qui commence,
# elle place son mot forcément en 7,7. Pas de dégrés de rélféxion.



#Une fous cela fait, on choisir le score max (ou presque max si on bride l'IA)
#On lui fait placer les lettres, on actualise les scores, on lui fait tirer ses lettres, et on passe
# la main au prochain ordi/joueur




#Algorithme de recherche dans une liste triée

def appartient (mot,liste):
    fin=len(liste)-1
    debut=0
    while abs(debut-fin)>1 :
        k=(debut+fin)//2
        if liste[k]>=mot:
            fin=k
        else:
            debut=k
    return (mot==liste[fin] or mot==liste[debut])






def balayagetotal ():
    res=[]
    for j in range(0,15):
        for i in range(0,8): #On balaye ligne à ligne
            res.append([(i,j),(i+1,j),(i+2,j),(i+3,j),(i+4,j),(i+5,j),(i+6,j),(i+7,j)])
            res.append([(j,i),(j,i+1),(j,i+2),(j,i+3),(j,i+4),(j,i+5),(j,i+6),(j,i+7)]) #Colonne à colonne
    return res

#Applique la règle des voisins, et enlève des coups possibles tous les coups dans le vide.
#Fonctionne dans le cas ou M[7][7] est remplie.
#Prend en argument les coups possibles et en purgent les coups impossibles



def reglevoisinsvide (l):
    res=[]
    if M[7][7]!="":
        for e in l:
            if toutvoisins(e)!=[]:
                res.append(e)
    else:
        for e in l:
            if (7,7) in e:
                res.append(e)
    return res

def contientlettre(l):
    res=False
    for (i,j) in l:
        res=res or (M[i][j]!="")
    return res


def toutmotspeutjouer (toutmots,tirage,coupspossibles):
    res=[]
    lettresseules=toutes_lettres_simples(tirage)
    for e in toutmots+lettresseules: #Le lettres_seules est la pour considérer de ne jouer qu'une seule lettre
        #Si on a un joker, alors il faut ajouter toutes les lettres minuscules :)
        for coup in coupspossibles:
            (bool,lettreetplacement_etscore)=peutplacer(e,tirage,coup)
            if bool:
                res.append(lettreetplacement_etscore)
    return liste_purge(res)


def toutes_lettres_simples(tirage0):
    l=[]
    for e in tirageO:
        if e!="":
            if e=="?":
                l=l+list(verif)
            else:
                l.append(e)
    return l



def peutplacer(mot,tirage,coup):
    bool=True
    lettreetplacement_etscore=[[],0]
    k=8-len(mot)
    restant=(tirage)+[]
    for p in range(0,k+1):
        restant=list(tirage)
        placement=coup[p:p+len(mot)]
        res=[] #Va contenir lettre et placement
        i=0
        decale_mot=False
        tempoplacee=[]
        if ((7,7) in placement) or(toutvoisins(placement)!=[]): #Regle de contact avec les pièces du plateau
            #Ou alors on a encore jamais joué, et la seule règle et de placer un pion en (7,7)
            for lettre in mot:
                (ii,jj)=placement[i]
                if M[ii][jj]==lettre:
                    #Si au placement du mot, une lettre sur le plateau correspond exactement a la lettre que je veux jouer,
                    #Alors je ne joue pas la lettre, je ne la place pas, mais je peux voir si je peux jouer mon coup
                    placement.remove(placement[i])
                    #i=i+1 sous entendu dans le remove !
                elif M[ii][jj]!="":  #Alors on peut pas placer le mot, une lettre déjà placée nous empeche de le faire
                    decale_mot=True  #On passe au mot suivant
                    efface(tempoplacee)
                    i=0
                    break  #On arrete la boucle
                elif lettre in restant:
                    res.append((lettre,placement[i]))
                    restant.remove(lettre)
                    tempoplacee.append((ii,jj))
                    M[ii][jj]=lettre
                    i=i+1
                elif "?" in restant:  #Je peux éventuellement placer un Joker, si j'en ai un
                    res.append((minmaj(lettre),placement[i]))
                    restant.remove("?")
                    tempoplacee.append((ii,jj))
                    M[ii][jj]=minmaj(lettre)
                    i=i+1
                else:  #Else on est dans le cas qu'on ne possède pas la lettre pour le poser
                    decale_mot=True
                    efface(tempoplacee)
                    i=0
                    break
            if not decale_mot:  #Si on peut placer le mot
                #On doit vérifier que les voisins sont dans le lexique, et faire les scores proprement
                mot_sco=scores(placement) #On regarde le score
                (OK,sco)=danslex(mot_sco)
                efface(tempoplacee)
                if OK or (7,7) in placement: #Si le coup est valable
                    if (sco)>(lettreetplacement_etscore[1]):
                        lettreetplacement_etscore=[res,sco]
    if lettreetplacement_etscore==[[],0]:  #Si on n'a pas pu placer le mot
        bool=False
    return (bool,lettreetplacement_etscore)


#efface dans M les coordonnées tempo

def efface (tempo):
    global M
    for (i,j) in tempo:
        M[i][j]=""



def danslex (mot_sco):
    res=True
    total=0
    for ([m],sco) in mot_sco:
        if (m!="") and appartient (majminmot(m),lexique):
            total=total+sco
        else:
            res=False
            break
    return (res,total)


def meilleurs_coups (coupsposs):
    res=[]
    bestsco=0
    for (coup,sco) in coupsposs:
        if sco>bestsco:
            res=[coup]
            bestsco=sco
        if sco==bestsco:
            res.append(coup)
    return (res,bestsco)


def choix (meilleurcoup):
    (mots,sco)=meilleurcoup
    motelu=random_el(mots)
    return (motelu,sco)


def joue (ajouer):
    global tirageO
    affichecoupordi=[]
    for (lettre,place) in ajouer[0]:
        affichecoupordi.append(place)
        (i,j)=place
        M[i][j]=lettre
        can.create_text(i*40+20,j*40+20,text=lettre)
        can.create_text(i*40+30,j*40+30,text=pts[lettre])
        if lettre in verif:
            enleve(tirageO,"?")
        else:
            enleve(tirageO,lettre)
    affichecoup_ordi(scores(affichecoupordi))


def affichecoup_ordi (l):
    global ScoreO
    res="Ordinateur a joué : "
    tot=0
    for e in l:
        (mot,sco)=e
        tot=tot+sco
        mot=mot[0]
        res=res+mot+" (" + str(sco)+"), "
    ScoreO=ScoreO+tot
    effacemess()
    affiche_score()
    can.create_text(300,15*40+20,text=res[:len(res)-2])
    actuhisto("Ordi : "+res[20:len(res)-2])   #Actualisation de l'historique



#Programme principal de l'IA
def ordi():
    global justepasse,ORDI
    ORDI=True
    suspendvrai()
    couppossibles=balayagetotal()
    couppossibles=reglevoisinsvide(couppossibles)
    nbjoker=combien_joker(tirageO)
    if nbjoker==2:  #Si l'ordi a dejà 2 jokers, je ne lui rajoute pas de degré de réfléxion. Ses jokers le "font" déjà
        toutmots=tousmots(lexique,tirageO)
    else:
        toutmots=tousmots(lexique,tirageO+["?"]) #Sinon je peux lui rajouter un degré de réfléxion,
        # notemment pour pouvoir utiliser des lettres du plateau
    coupspossibles=(toutmotspeutjouer(toutmots,tirageO,couppossibles))
    bestcoups=(meilleurs_coups(coupspossibles))
    if bestcoups==([],0):
        passeO()
        reactive()
    else:
        ajouer=choix(bestcoups)
        joue(ajouer)
        (bool,gagnant)=est_victoire()
        justepasse=False
        if bool:
            victoire(gagnant)
        else:
            tireO()
            affiche_lettres_rest()
            reactive()
    ORDI=False







#========================= Sauvegarde de votre meilleur score





# Universel selon les langues : Pour rechercher le meilleur score et éventuellement l'enregistrer

def get_best_score():
  global scoremax,motlu,scoremot,langue
  try:
    f=open("scores"+langue+".txt","r")
    f.readline()  #On vire l'entête
    scoremax=0
    motlu=""
    scoremot=0
    scomax=f.readline()
    essmot=f.readline()
    essmot=essmot[:len(essmot)-1]
    scomot=f.readline()
    while scomax!="" and essmot !="" and scomot!="":
        try:
            scoremax=max(scoremax,int(scomax))
            temp=int(scomot)
            if temp>scoremot:
                motlu=essmot
                scoremot=temp
        except:
            ()
        try:
            scomax=f.readline()
            essmot=f.readline()
            scomot=f.readline()
        except:
            scomax=""
            essmot=""
            scomot=""
    f.close()

  except:
    scoremax=0
    motlu=""
    scoremot=0
    f=open("scores"+langue+".txt","w")
    f.write("Historique des meilleurs scores du jeu en Français ! :)")
    f.close()




def enregistre():
    global ScoreJ,meilleurscoremot,meilleurmot,scoremot,scoremax,motlu,langue
    doissauver=False
    if ScoreJ>scoremax:
        scoremax=ScoreJ
        doissauver=True
    if meilleurscoremot>scoremot:
        doissauver=True
        scoremot=meilleurscoremot
        motlu=meilleurmot
    if doissauver:
        f=open("scores"+langue+".txt","r")  #je prends tout pour tout recopier
        tout=f.read()
        f.close()
        f=open("scores"+langue+".txt","w")
        f.write(tout+"\n")
        f.write(str(scoremax)+"\n")
        f.write(motlu+"\n")
        f.write(str(scoremot))
        f.close()

def changemot (mot,sco):
    global meilleurmot,meilleurscoremot
    if mot!="":
        if sco>meilleurscoremot:
            meilleurmot=mot
            meilleurscoremot=sco



#====================== PROGRAMMES PRINCIPAUX GESTION DES FENETRES


#Menu principal, accueil




def menu():
    global fnm,Langues,liste
    fnm=Tk()
    fnm.title("Bienvenue au jeu de Scrabble !")
    text=Label(fnm,text="Bienvenue au jeu de Scrabble !")
    text.grid(row=0,column=0,columnspan=2)
    text3=Label(fnm,text="Choisissez votre langue de jeu")
    text3.grid(row=1,column=0,columnspan=2)
    frame = Frame(fnm,width=300,height=300)
    frame.grid(row=2,column=0,columnspan=2)
    liste = Listbox(frame) # je crée ma liste
    liste.pack(side=LEFT, expand=YES, fill=BOTH)
    bval=Button(fnm, text='Valider', command=choixlangue)
    bval.grid(row=3,column=0,columnspan=2)
    for index in range(0,8):  # j'insère dans ma liste les différents choix
        liste.insert(index,Langues[index] )
    text4=Label(fnm,text="Je vous souhaite bon jeu, et signalez-moi tout bug s'il vous plait, merci :)")
    text4.grid(row=4,column=0,columnspan=2)
    text5=Label(fnm,text="IMPORTANT : Si parfois, vous ne parvenez plus à cliquer sur le plateau, ")
    text5.grid(row=5,column=0,columnspan=2)
    text6=Label(fnm,text="appuyer sur le bouton 'Rappelle' corrigera le problème ! ;) ")
    text6.grid(row=6,column=0,columnspan=2)
    bquit=Button(fnm,text="Quit",command=fnm.destroy)
    bquit.grid(row=7,column=0,columnspan=2)
    text5=Label(fnm,text="© Julien Oury--Nogues")
    text5.grid(row=8,column=0,columnspan=2)
    fnm.mainloop()



# GESTION DE TOUTES LES LANGUES PROPOSEES

Langues=["Français","Anglais","Allemand","Espagnol","Italien","Néerlandais","Portugais","Latin"]


def choixlangue ():
    global fnm,liste,frame
    choix=(liste.get(ACTIVE))  # on récupère le choix de l'utilisateur
    if choix=="Français":
        francais()
    if choix=="Anglais":
        anglais()
    if choix=="Allemand":
        allemand()
    if choix=="Espagnol":
        espagnol()
    if choix=="Italien":
        italien()
    if choix=="Néerlandais":
        neerlandais()
    if choix=="Portugais":
        portugais()
    if choix=="Latin":
        latin()


#Langue française

def francais ():
    global lexique,pts,points,proba,A,sac,langue,alphabet
    fnm.destroy()
    langue="FR"
    alphabet= ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","?")
    get_best_score() #je charge les meilleurs scores français
    # Importation du lexique français
    f=open("lexiqueFR.txt","r")
    l=f.readline()
    lexique = list()
    while l[:len(l)-1]!= "":
        lexique.append(l[:len(l)-1])
        l=f.readline()
    f.close()    #Le lexique est stocké dans une liste
    points=(1,3,3,2,1,4,2,4,1,8,10,1,2,1,1,3,8,1,1,1,1,4,10,10,10,10,0)
    proba=(10,2,2,3,15,2,2,2,8,1,1,5,3,6,6,2,1,6,6,6,6,2,1,1,1,1,2)
    #pts est le score associé à chaque lettre selon les règles du Scrabble
    pts={}
    for i in range(0,len(alphabet)):
        pts[alphabet[i]]=points[i]
        pts[minmaj(alphabet[i])]=0   # Toutes les minuscules seront des jokers utilisés et valent 0 pts
    #nécessaire pour un tirage parfaitement aléatoire
    A=[(x,y) for (x,y) in zip(alphabet,proba)]
    sac=toutes_lettres(A)
    #en jeu !
    premierepartie()



# Langue anglaise

def anglais ():
    global lexique,pts,points,proba,A,sac,langue,alphabet
    fnm.destroy()
    alphabet= ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","?")
    langue="AN"
    get_best_score() #je charge les meilleurs scores anglais
    # Importation du lexique anglais
    f=open("lexiqueAN.txt","r")
    l=f.readline()
    lexique = list()
    while l[:len(l)-1]!= "":
        lexique.append(l[:len(l)-1])
        l=f.readline()
    f.close()    #Le lexique est stocké dans une liste
    points=(1,3,3,2,1,4,2,4,1,8,5,1,3,1,1,3,10,1,1,1,1,4,4,8,4,10,0)
    proba=(9,2,2,4,12,2,3,2,9,1,1,4,2,6,8,2,1,6,4,6,4,2,2,1,2,1,2)
    #pts est le score associé à chaque lettre selon les règles du Scrabble
    pts={}
    for i in range(0,len(alphabet)):
        pts[alphabet[i]]=points[i]
        pts[minmaj(alphabet[i])]=0   # Toutes les minuscules seront des jokers utilisés et valent 0 pts
    #nécessaire pour un tirage parfaitement aléatoire
    A=[(x,y) for (x,y) in zip(alphabet,proba)]
    sac=toutes_lettres(A)
    #en jeu !
    premierepartie()

#Espagnol

def espagnol ():
    global lexique,pts,points,proba,A,sac,langue,alphabet
    fnm.destroy()
    langue="ES"
    alphabet= ("A","B","C","CH","D","E","F","G","H","I","J","K","L","LL","M","N","O","P","Q","R","RR","S","T","U","V","W","X","Y","Z","?")
    get_best_score () #je charge les meilleurs scores français
    # Importation du lexique français
    f=open("lexiqueES.txt","r")
    l=f.readline()
    lexique = list()
    while l[:len(l)-1]!= "":
        lexique.append(l[:len(l)-1])
        l=f.readline()
    f.close()    #Le lexique est stocké dans une liste
    points=(1,3,3,5,2,1,4,2,4,1,8,8,1,8,3,1,1,3,5,1,8,1,1,1,4,8,8,4,10,0)
    proba=(12,3,4,1,5,12,2,2,2,6,2,1,4,1,3,6,9,2,1,5,1,7,4,6,2,1,1,1,1,2)
    #pts est le score associé à chaque lettre selon les règles du Scrabble
    pts={}
    for i in range(0,len(alphabet)):
        pts[alphabet[i]]=points[i]
        pts[minmaj(alphabet[i])]=0   # Toutes les minuscules seront des jokers utilisés et valent 0 pts
    #nécessaire pour un tirage parfaitement aléatoire
    A=[(x,y) for (x,y) in zip(alphabet,proba)]
    sac=toutes_lettres(A)
    #en jeu !
    premierepartie()

#Langue allemande

def allemand ():
    global lexique,pts,points,proba,A,sac,langue,alphabet
    fnm.destroy()
    langue="ALL"
    alphabet= ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","?")
    get_best_score() #je charge les meilleurs scores
    # Importation du lexique allemand
    f=open("lexiqueALL.txt","r")
    l=f.readline()
    lexique = list()
    while l[:len(l)-1]!= "":
        lexique.append(l[:len(l)-1])
        l=f.readline()
    f.close()    #Le lexique est stocké dans une liste
    points=(1,3,4,1,1,4,2,2,1,6,4,2,3,1,2,4,10,1,1,1,1,6,3,8,10,3,0)
    proba=(6,2,2,4,15,2,3,4,6,1,2,3,4,9,4,1,1,6,7,6,7,1,1,1,1,1,2)
    #pts est le score associé à chaque lettre selon les règles du Scrabble
    pts={}
    for i in range(0,len(alphabet)):
        pts[alphabet[i]]=points[i]
        pts[minmaj(alphabet[i])]=0   # Toutes les minuscules seront des jokers utilisés et valent 0 pts
    #nécessaire pour un tirage parfaitement aléatoire
    A=[(x,y) for (x,y) in zip(alphabet,proba)]
    sac=toutes_lettres(A)
    #en jeu !
    premierepartie()

#Italien

def italien ():
    global lexique,pts,points,proba,A,sac,langue,alphabet
    fnm.destroy()
    langue="IT"
    alphabet= ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","?")
    get_best_score() #je charge les meilleurs scores
    # Importation du lexique allemand
    f=open("lexiqueIT.txt","r")
    l=f.readline()
    lexique = list()
    while l[:len(l)-1]!= "":
        lexique.append(l[:len(l)-1])
        l=f.readline()
    f.close()    #Le lexique est stocké dans une liste
    points=(1,5,2,5,1,5,8,8,1,10,10,3,3,3,1,5,10,2,2,2,3,5,10,10,10,8,0)
    proba=(14,3,6,3,11,3,2,2,12,1,1,5,5,5,15,3,1,6,6,6,5,3,1,1,1,2,2)
    #pts est le score associé à chaque lettre selon les règles du Scrabble
    pts={}
    for i in range(0,len(alphabet)):
        pts[alphabet[i]]=points[i]
        pts[minmaj(alphabet[i])]=0   # Toutes les minuscules seront des jokers utilisés et valent 0 pts
    #nécessaire pour un tirage parfaitement aléatoire
    A=[(x,y) for (x,y) in zip(alphabet,proba)]
    sac=toutes_lettres(A)
    #en jeu !
    premierepartie()


# Latin

def latin ():
    global lexique,pts,points,proba,A,sac,langue,alphabet
    fnm.destroy()
    langue="LAT"
    alphabet= ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","?")
    get_best_score() #je charge les meilleurs scores
    # Importation du lexique allemand
    f=open("lexiqueLAT.txt","r")
    l=f.readline()
    lexique = list()
    while l[:len(l)-1]!= "":
        lexique.append(l[:len(l)-1])
        l=f.readline()
    f.close()    #Le lexique est stocké dans une liste
    points=(1,4,2,2,1,8,4,8,1,10,10,2,2,2,1,4,3,1,1,1,1,1,10,4,10,10,0)
    proba=(9,2,4,3,12,1,2,1,9,0,1,3,4,4,5,2,3,7,8,8,9,9,0,2,1,1,2)
    #pts est le score associé à chaque lettre selon les règles du Scrabble
    pts={}
    for i in range(0,len(alphabet)):
        pts[alphabet[i]]=points[i]
        pts[minmaj(alphabet[i])]=0   # Toutes les minuscules seront des jokers utilisés et valent 0 pts
    #nécessaire pour un tirage parfaitement aléatoire
    A=[(x,y) for (x,y) in zip(alphabet,proba)]
    sac=toutes_lettres(A)
    #en jeu !
    premierepartie()

# Neerlandais

def neerlandais ():
    global lexique,pts,points,proba,A,sac,langue,alphabet
    fnm.destroy()
    langue="NL"
    alphabet= ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","?")
    get_best_score() #je charge les meilleurs scores
    # Importation du lexique allemand
    f=open("lexiqueNL.txt","r")
    l=f.readline()
    lexique = list()
    while l[:len(l)-1]!= "":
        lexique.append(l[:len(l)-1])
        l=f.readline()
    f.close()    #Le lexique est stocké dans une liste
    points=(1,3,5,2,1,4,3,4,1,4,3,3,3,1,1,3,10,2,2,2,4,4,5,8,8,4,0)
    proba=(6,2,2,5,18,1,3,2,6,3,3,3,3,10,6,2,1,5,4,5,3,2,2,1,1,2,2)
    #pts est le score associé à chaque lettre selon les règles du Scrabble
    pts={}
    for i in range(0,len(alphabet)):
        pts[alphabet[i]]=points[i]
        pts[minmaj(alphabet[i])]=0   # Toutes les minuscules seront des jokers utilisés et valent 0 pts
    #nécessaire pour un tirage parfaitement aléatoire
    A=[(x,y) for (x,y) in zip(alphabet,proba)]
    sac=toutes_lettres(A)
    #en jeu !
    premierepartie()

# Portugais

def portugais ():
    global lexique,pts,points,proba,A,sac,langue,alphabet
    fnm.destroy()
    langue="PT"
    alphabet= ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","?")
    get_best_score() #je charge les meilleurs scores
    # Importation du lexique allemand
    f=open("lexiquePT.txt","r")
    l=f.readline()
    lexique = list()
    while l[:len(l)-1]!= "":
        lexique.append(l[:len(l)-1])
        l=f.readline()
    f.close()    #Le lexique est stocké dans une liste
    points=(1,3,2,2,1,4,4,4,1,5,10,2,1,3,1,2,6,1,1,1,1,4,10,8,10,8,0)
    proba=(14,3,6,5,5,2,2,2,10,2,1,5,6,4,10,4,1,6,6,8,7,2,1,1,1,1,3)
    #pts est le score associé à chaque lettre selon les règles du Scrabble
    pts={}
    for i in range(0,len(alphabet)):
        pts[alphabet[i]]=points[i]
        pts[minmaj(alphabet[i])]=0   # Toutes les minuscules seront des jokers utilisés et valent 0 pts
    #nécessaire pour un tirage parfaitement aléatoire
    A=[(x,y) for (x,y) in zip(alphabet,proba)]
    sac=toutes_lettres(A)
    #en jeu !
    premierepartie()




#Gère l'éventuelle nouvelle partie, et l'éventuel retour au menu (appui sur bouton)

#Dans les deux cas, je dois vider le plateau et la réglette. Allons-y

def vide_plateau():
    global M
    M=make_matrix(15)

def vide_reglette():
    global tirageO,tirageJ
    tirageJ=[""]*7
    tirageO=[""]*7


#Nouvelle partie


def newconf():
    global fenouverte,fnew
    ferme_tout()
    fenouverte=(True,"fnew")
    fnew=Tk()
    fnew.title("Confirmation")
    text=Label(fnew,text="Êtes-vous sûr de commencer une nouvelle partie ?")
    text.grid(row=0,column=0,columnspan=2)
    text2=Label(fnew,text="L'avancement de cette partie serait perdu")
    text2.grid(row=1,column=0,columnspan=2)
    by=Button(fnew,text="Oui",command=newpart)
    by.grid(row=2,column=0)
    bn=Button(fnew,text="Non",command=fnewquit)
    bn.grid(row=2,column=1)
    fnew.mainloop()

def fnewquit():
    global fenouverte,fnew
    fenouverte=(False,"")
    fnew.destroy()

def newpart():
    global ScoreJ,ScoreO,sac
    fnewquit()
    fen.destroy()
    vide_plateau()
    vide_reglette()
    ScoreJ=0  # reset des scores
    ScoreO=0
    sac=toutes_lettres(A) #reset du sac
    premierepartie()



#Retour au menu


def menuconf():
    global fenouverte,fmenu
    ferme_tout()
    fenouverte=(True,"fmenu")
    fmenu=Tk()
    fmenu.title("Confirmation")
    text=Label(fmenu,text="Êtes-vous sûr de vouloir revenir au menu ?")
    text.grid(row=0,column=0,columnspan=2)
    text2=Label(fmenu,text="L'avancement de cette partie serait perdu")
    text2.grid(row=1,column=0,columnspan=2)
    by=Button(fmenu,text="Oui",command=menupart)
    by.grid(row=2,column=0)
    bn=Button(fmenu,text="Non",command=fmenuquit)
    bn.grid(row=2,column=1)
    fmenu.mainloop()

def fmenuquit():
    global fenouverte,fmenu
    fenouverte=(False,"")
    fmenu.destroy()

def menupart():
    global ScoreJ,ScoreO,sac
    fmenuquit()
    vide_plateau()
    vide_reglette()
    fen.destroy()
    ScoreJ=0 #reset des scores
    ScoreO=0
    sac=toutes_lettres(A) #reset du sac
    menu()



#Actualise l'historique

def actuhisto (txt):
    global coup
    histo.insert(coup," "+str(coup)+". "+txt)
    coup=coup+1

#Confirmation de quitter le jeu


def fenquitconf ():
    global fquit,fenouverte
    ferme_tout()
    fenouverte=(True,"fquit")
    fquit=Tk()
    text=Label(fquit,text="Êtes-vous sûr de vouloir quitter ?")
    text.grid(row=0,column=0,columnspan=2)
    text2=Label(fquit,text="L'avancement de la partie sera perdu.")
    text2.grid(row=1,column=0,columnspan=2)
    by=Button(fquit,text="Oui",command=fenquit)
    by.grid(row=2,column=0)
    bn=Button(fquit,text="Non",command=quitconf)
    bn.grid(row=2,column=1)
    fquit.mainloop()

def quitconf ():
    global fquit
    fenouverte=(False,"")
    fquit.destroy()

def fenquit ():
    global fen
    quitconf()
    fen.destroy()


#Programme principal, en cours de partie !


def premierepartie ():
    global ORDI,fen,can,bt,bp,b1let,btout,blex,bmix,brap,bq,bmenu,bnew,premier_coup,justepasse,coup,histo,scoremot,scoremax,motlu,meilleurscoremot,meilleurmot
    #nécessaire pour le premier tirage.
    premier_coup=True
    #Nécessaire pour la gestion du match nul. Tout le monde passe
    justepasse=False
    #Compteur pour l'historique
    meilleurscoremot=0
    meilleurmot=""
    coup=0
    ORDI=False
    fen= Tk()
    fen.title("Jeu de Scrabble")
    can=Canvas(fen,bg='ivory',height=700, width=600)
    can.grid(row =0, column =0, rowspan =10, padx =10, pady =5)
    can.bind("<Button-1>", select) #clic gauche
    can.bind("<Button-3>", cancel) #clic droit
    bt=Button(fen,text="Validation",command=jeu)
    bt.grid(row=0,column=1)
    bp=Button(fen,text="Passer",command=passeconf)
    bp.grid(row=1,column=1)
    b1let=Button(fen,text="Echanger une lettre",command=echange1)
    b1let.grid(row=2,column=1)
    btout=Button(fen,text="Echanger 7 lettres",command=echangetout)
    btout.grid(row=3,column=1)
    blex=Button(fen,text="Lexique",command=ouvre_lexique)
    blex.grid(row=4,column=1)
    bmix=Button(fen,text="Mélanger",command=melange)
    bmix.grid(row=5,column=1)
    brap=Button(fen,text="Rappelle",command=rappelle)
    brap.grid(row=6,column=1)
    bnew=Button(fen,text="Nouvelle Partie",command=newconf)
    bnew.grid(row=7,column=1)
    bmenu=Button(fen,text="Menu",command=menuconf)
    bmenu.grid(row=8,column=1)
    bq=Button(fen,text="Quit",command=fenquitconf)
    bq.grid(row=9,column=1)
    texthist=Label(fen,text="Historique de jeu")
    texthist.grid(row=2,column=2)
    frame = Frame(fen)
    frame.grid(row=2,column=2,rowspan=5)
    histo = Listbox(frame) # je crée ma liste
    sbar = Scrollbar(frame) # Ma scrollbar vericale
    sbar.config(orient=VERTICAL,command=histo.yview)
    sbar2 = Scrollbar(frame) # Ma scrollbar horizontale
    sbar2.config(orient=HORIZONTAL,command=histo.xview)
    histo.config(yscrollcommand=sbar.set)
    sbar.pack(side=RIGHT, fill=Y)
    sbar2.pack(side=BOTTOM,fill=X)
    histo.pack(side=LEFT, expand=YES, fill=BOTH)
    #les scores
    scoB=Label(fen,text="Vos meilleurs scores !")
    scoB.grid(row=6,column=2)
    scoB2=Label(fen,text="Meilleure partie : "+str(scoremax))
    scoB2.grid(row=7,column=2)
    scoM=Label(fen,text="Meilleur mot joué : ")
    scoM.grid(row=8,column=2)
    scoM2=Label(fen,text=motlu+" ("+str(scoremot)+" points)")
    scoM2.grid(row=9,column=2)
    plateau()
    jeu() #Je tire les lettres pour tout le monde
    affiche_score()
    affiche_lettres_rest()
    fen.mainloop()


# C'est parti !

menu()









