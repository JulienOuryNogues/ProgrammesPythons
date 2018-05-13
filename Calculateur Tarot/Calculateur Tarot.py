__author__ = 'Julien'

from tkinter import *
from tkinter.ttk import *
from tkinter import ttk



#Contient tous les scores temporaires

M=[]


# Contient tous les scores totaux à chaque étape

P=[]


def nb_joueurs():
    global entree,fennb
    fennb=Tk()
    fennb.title("Nombre de joueurs")
    text=Label(fennb,text="Veuillez entrer le nombre de joueurs de cette partie (entre 3 et 5)")
    text.pack()
    entree = Entry(fennb)
    entree.bind("<Return>", nomjoueurs)
    entree.pack()
    text2=Label(fennb,text="Et appuyez sur Entrée")
    text2.pack()
    fennb.mainloop()


def nomjoueurs(event):
    global entree,N,fennb,fenm,Lscotot
    a=int(entree.get())
    if a in range(3,6):
        N=a
        Lscotot=[0]*N
        M.append([0]*N)
        P.append([0]*N)
        fennb.destroy()
        fenm=Tk()
        fenm.title("Nom des joueurs")
        text=Label(fenm,text="Veuillez entrer les noms des joueurs séparés par un espace ")
        text.pack()
        entree = Entry(fenm)
        entree.bind("<Return>", principal)
        entree.pack()
        text2=Label(fenm,text="Et appuyez sur Entrée")
        text2.pack()
        fennb.mainloop()


def principal(event):
    global entree,L,N,fenm,can,quelleligne
    A=entree.get()
    L=A.split()  #Liste des noms des joueurs
    quelleligne=2
    if len(L)==N:
        fenm.destroy()
        fen=Tk()
        fen.title("Fenêtre principale")
        can=Canvas(fen,bg='ivory',height=800, width=100*N)
        can.grid(row=0,column=0,rowspan=4)
        dessintableau(can)
        bnew=Button(fen,text="Nouvelle Partie",command=nouvelle_partie)
        bnew.grid(row=0,column=2)
        bmis=Button(fen,text="Misère",command=misere)
        bmis.grid(row=1,column=2)
        ban=Button(fen,text="Annule",command=confanul)
        ban.grid(row=2,column=2)
        bgr=Button(fen,text="Graphe",command=dessin_graphe)
        bgr.grid(row=3,column=2)


# Bouton Misere

def misere():
    global fmis,liste
    fmis=Tk()
    fmis.title("Menu misère")
    text=Label(fmis,text="Choisissez le joueur bénéficiaire")
    text.grid(row=0,column=0)
    frame = Frame(fmis,width=300,height=300)
    frame.grid(row=1,column=0)
    liste = Listbox(frame) # je crée ma liste
    liste.pack(side=LEFT, expand=YES, fill=BOTH)
    bval=Button(fmis, text='Valider', command=bonusmis)
    bval.grid(row=2,column=0)
    for index in range(0,N):  # j'insère dans ma liste les différents choix
        liste.insert(index,L[index])
    fmis.mainloop()


def bonusmis():
    global fmis,liste,N,L,Lscotemp,Lscotot,M
    benef=liste.get(ACTIVE)
    fmis.destroy()
    Lscotemp=[0]*N
    for i in range(N):
        if L[i]==benef:
            Lscotot[i]+=10*(N-1)
            Lscotemp[i]=10*(N-1)
        else:
            Lscotot[i]-=10
            Lscotemp[i]=-10
    M.append(list(Lscotemp))
    P.append(list(Lscotot))
    affichenew()
    affichetot()



#Gere le dessin du tableau de la fenêtre principale

def dessintableau(can):
    global L,N
    for i in range(0,100*N,100):
        can.create_line(i,0,i,2000,fill="black")
        can.create_text(i+50,10,text=L[i//100]+" ("+Lcolor[i//100]+")")
    can.create_line(0,20,100*N,20)


#Bouton annuler

def confanul():
    global fan
    fermegraphe()
    if len(M)>0:
        fan=Tk()
        fan.title("Confirmation annulation")
        text=Label(fan,text="Êtes-vous sûr de vouloir annuler la dernière partie ?")
        text.grid(row=0,column=0,columnspan=2)
        bo=Button(fan,text="Oui",command=annule)
        bo.grid(row=1,column=0)
        bn=Button(fan,text="Non",command=fan.destroy)
        bn.grid(row=1,column=1)
        fan.mainloop()

def annule():
    global quelleligne,M,Lscotot,fan,P
    fan.destroy()
    fermegraphe()
    if len(M)>1:
        Lsupr=M[len(M)-1]
        quelleligne-=1 #On remonte d'une ligne
        for i in range(N):
            Lscotot[i]-=Lsupr[i] #On supprime la dernière ligne
            can.create_rectangle(100*i+1,20*quelleligne+1,100*(i+1)-1,20*(quelleligne+1)-1,fill="ivory",outline="ivory")
            #On efface la dernière ligne
        affichetot() #on actualise les scores
        M=M[:len(M)-1]
        P=P[:len(P)-1]




#Gere le bouton nouvelle partie et toute la suite

def nouvelle_partie():
    global N,L,liste,fp
    fermegraphe()
    fp=Tk()
    fp.title("Nouvelle partie : choix preneur")
    text=Label(fp,text="Choisissez le preneur")
    text.grid(row=0,column=0)
    frame = Frame(fp,width=300,height=300)
    frame.grid(row=1,column=0)
    liste = Listbox(frame) # je crée ma liste
    liste.pack(side=LEFT, expand=YES, fill=BOTH)
    bval=Button(fp, text='Valider', command=choixsuite)
    bval.grid(row=2,column=0)
    for index in range(0,N):  # j'insère dans ma liste les différents choix
        liste.insert(index,L[index])
    fp.mainloop()



def choixsuite ():
    global liste,N,L,fp,preneur
    fermegraphe()
    preneur=(liste.get(ACTIVE))
    fp.destroy()
    if N==5:
        fp=Tk()
        fp.title("Nouvelle partie : choix équipier")
        text=Label(fp,text="Choisissez l'équipier")
        text.grid(row=0,column=0)
        frame = Frame(fp,width=300,height=300)
        frame.grid(row=1,column=0)
        liste = Listbox(frame) # je crée ma liste
        liste.pack(side=LEFT, expand=YES, fill=BOTH)
        bval=Button(fp, text='Valider', command=choixcontrat)
        bval.grid(row=2,column=0)
        for index in range(0,N):  # j'insère dans ma liste les différents choix
            liste.insert(index,L[index])
        fp.mainloop()
    else:
        choixcontrat()


Lcontrat=["Petite","Garde","Garde Sans","Garde Contre"]

def choixcontrat():
    fermegraphe()
    global fp,liste,Lcontrat,equipier,fcon
    if N==5:
        equipier=(liste.get(ACTIVE))
        fp.destroy()
    else:
        equipier="Aucun"
    fcon=Tk()
    fcon.title("Nouvelle partie : choix contrat")
    text=Label(fcon,text="Quel contrat ?")
    text.grid(row=0,column=0)
    frame = Frame(fcon,width=300,height=300)
    frame.grid(row=1,column=0)
    liste = Listbox(frame) # je crée ma liste
    liste.pack(side=LEFT, expand=YES, fill=BOTH)
    bval=Button(fcon, text='Valider', command=reussi)
    bval.grid(row=2,column=0)
    for index in range(0,4):  # j'insère dans ma liste les différents choix
        liste.insert(index,Lcontrat[index])
    fcon.mainloop()

def reussi():
    fermegraphe()
    global contrat,liste,fcon,fres
    contrat=liste.get(ACTIVE)
    fcon.destroy()
    fres=Tk()
    fres.title("Nouvelle partie : contrat rempli ?")
    text=Label(fres,text="Contrat rempli ?")
    text.grid(row=0,column=0,columnspan=2)
    bo=Button(fres,text="Oui",command=passe)
    bo.grid(row=1,column=0)
    bn=Button(fres,text="Non",command=chute)
    bn.grid(row=1,column=1)
    fres.mainloop()

def passe ():
    global contratrempli,fres,fpoints,entree
    fermegraphe()
    fres.destroy()
    contratrempli=True
    fpoints=Tk()
    fpoints.title("Nouvelle partie : points")
    text=Label(fpoints,text="Contrat passé de ?")
    text.pack()
    entree = Entry(fpoints)
    entree.bind("<Return>", petitbout)
    entree.pack()
    text2=Label(fpoints,text="Et appuyez sur Entrée")
    text2.pack()
    fpoints.mainloop()

def chute ():
    global contratrempli,fres,fpoints,entree
    fermegraphe()
    fres.destroy()
    contratrempli=False
    fpoints=Tk()
    fpoints.title("Nouvelle partie : points")
    text=Label(fpoints,text="Contrat chuté de ?")
    text.pack()
    entree = Entry(fpoints)
    entree.bind("<Return>", petitbout)
    entree.pack()
    text2=Label(fpoints,text="Et appuyez sur Entrée")
    text2.pack()
    fpoints.mainloop()


def petitbout(event):
    global fpet,fpoints,entree,points
    fermegraphe()
    points=float(entree.get())
    fpoints.destroy()
    fpet=Tk()
    fpet.title("Nouvelle partie : Petit")
    text=Label(fpet,text="Petit au bout ?")
    text.grid(row=0,column=0,columnspan=3)
    bo=Button(fpet,text="Attaque",command=bonus)
    bo.grid(row=1,column=0)
    bn=Button(fpet,text="Defense",command=malus)
    bn.grid(row=1,column=1)
    bn=Button(fpet,text="Non",command=rien)
    bn.grid(row=1,column=2)
    fpet.mainloop()


def bonus ():
    global petitaubout,fpet
    fermegraphe()
    fpet.destroy()
    petitaubout="Att"
    poignee()

def malus ():
    global petitaubout,fpet
    fermegraphe()
    fpet.destroy()
    petitaubout="Def"
    poignee()

def rien ():
    global petitaubout,fpet
    fermegraphe()
    fpet.destroy()
    petitaubout=""
    poignee()



Lpoignee=["Aucune","Simple","Double","Triple"]

def poignee():
    global Lpoignee,fpoi,liste
    fermegraphe()
    fpoi=Tk()
    fpoi.title("Nouvelle partie : Poignée")
    text=Label(fpoi,text="Poignée ?")
    text.grid(row=0,column=0)
    frame = Frame(fpoi,width=300,height=300)
    frame.grid(row=1,column=0)
    liste = Listbox(frame) # je crée ma liste
    liste.pack(side=LEFT, expand=YES, fill=BOTH)
    bval=Button(fpoi, text='Valider', command=autre)
    bval.grid(row=2,column=0)
    for index in range(0,4):  # j'insère dans ma liste les différents choix
        liste.insert(index,Lpoignee[index])
    fpoi.mainloop()


def autre():
    global fpoi, poignee1,liste
    fermegraphe()
    poignee1=liste.get(ACTIVE)
    fpoi.destroy()
    if poignee1!="Aucune":
        fpoi=Tk()
        fpoi.title("Nouvelle partie : Poignée")
        text=Label(fpoi,text="Seconde Poignée ?")
        text.grid(row=0,column=0)
        frame = Frame(fpoi,width=300,height=300)
        frame.grid(row=1,column=0)
        liste = Listbox(frame) # je crée ma liste
        liste.pack(side=LEFT, expand=YES, fill=BOTH)
        bval=Button(fpoi, text='Valider', command=chelem)
        bval.grid(row=2,column=0)
        for index in range(0,4):  # j'insère dans ma liste les différents choix
            liste.insert(index,Lpoignee[index])
        fpoi.mainloop()
    else:
        chelem()


Lchel=["Aucun","Annoncé réussi","Annoncé chuté","Non annoncé","Défensif"]
def chelem():
    global fpoi,liste,poignee2,fch
    fermegraphe()
    try:
        poignee2=liste.get(ACTIVE)
        fpoi.destroy()
    except:
        poignee2="Aucune"
    fch=Tk()
    fch.title("Nouvelle partie : Chelem")
    text=Label(fch,text="Chelem ?")
    text.grid(row=0,column=0)
    frame = Frame(fch,width=300,height=300)
    frame.grid(row=1,column=0)
    liste = Listbox(frame) # je crée ma liste
    liste.pack(side=LEFT, expand=YES, fill=BOTH)
    bval=Button(fch, text='Valider', command=calcul)
    bval.grid(row=2,column=0)
    for index in range(0,5):  # j'insère dans ma liste les différents choix
        liste.insert(index,Lchel[index])
    fch.mainloop()






def calcul ():
    global poignee1,poignee2,chelems,petitaubout,points,contratrempli,equipier,preneur,contrat,Lscotemp,N,L,fch,M,P
    chelems=liste.get(ACTIVE)
    fermegraphe()
    fch.destroy()
    Lscotemp=[0]*N
    res=25.
    points=float(points)
    res+=points
    if not(contratrempli):
        res=-res
    if petitaubout=="Att":
        res+=10
    if petitaubout=="Def":
        res-=10
    if contrat=="Garde":
        res=2*res
    if contrat=="Garde Sans":
        res=4*res
    if contrat=="Garde Contre":
        res=6*res
    if poignee1=="Simple":
        res+=20
    if poignee1=="Double":
        res+=30
    if poignee1=="Triple":
        res+=40
    if poignee2=="Simple":
        res+=20
    if poignee2=="Double":
        res+=30
    if poignee2=="Triple":
        res+=40
    if chelems=="Annoncé réussi":
        res+=400
    if chelems=="Annoncé chuté" or chelems=="Défensif":
        res-=200
    if chelems=="Non annoncé":
        res+=200
    if equipier==preneur or equipier=="Aucun":
        for i in range(N):
            if L[i]==preneur:
                Lscotot[i]+=(N-1)*res
                Lscotemp[i]=(N-1)*res
            else:
                Lscotot[i]-=res
                Lscotemp[i]=-res
    else:
        for i in range(N):
            if L[i]==preneur:
                Lscotot[i]+=(N-3)*res
                Lscotemp[i]=(N-3)*res
            elif L[i]==equipier:
                Lscotot[i]+=res
                Lscotemp[i]=res
            else:
                Lscotot[i]-=res
                Lscotemp[i]=-res
    M.append(list(Lscotemp))
    P.append(list(Lscotot))
    affichetot()
    affichenew()



def affichetot():
    global can
    for i in range(N):
        can.create_rectangle(100*i,20,100*(i+1),40,outline="black",fill="ivory")
        can.create_text(100*i+25,30,text=Lscotot[i])

def affichenew():
    global quelleligne
    for i in range(N):
        can.create_text(100*i+25,20*quelleligne+10,text=Lscotemp[i])
    quelleligne+=1



Lcolor=["red","blue","green","cyan","yellow"]


def fermegraphe():
    global fgraph
    try:
        fgraph.close()
    except:
        ()



def circle(can,x,y,r,color):
   return can.create_oval(x-r,y-r,x+r,y+r,fill=color)

def dessin_graphe():
    global P,quelleligne,fgraph
    fermegraphe()
    espacement=quelleligne-2
    n=len(P)
    if n>1:
        longueur=1300//espacement
        fgraph=Tk()
        fgraph.title("Les graphes ")
        can2=Canvas(fgraph,bg='ivory',height=800, width=1300)
        can2.pack()
        dessin_ligne(can2)
        m=len(P[0])
        R=5
        for j in range(m):
            for i in range(n-1):
                can2.create_line(i*longueur,-(P[i][j])//5+400,(i+1)*longueur,-(P[i+1][j])//5+400,fill=Lcolor[j])
                circle(can2,i*longueur,-(P[i][j])//5+400,R,Lcolor[j])
            circle(can2,(n-1)*longueur,-(P[n-1][j])//5+400,R,Lcolor[j])



def dessin_ligne(can):
    for i in range (0,801,100):
        can.create_line(0,i,1300,i)
        can.create_text(20,i-10,text=str((400-i)*5))


nb_joueurs()


