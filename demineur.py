from tkinter import *
from tkinter.messagebox import *
from random import *
from datetime import datetime
from time import *
from libs.playsound import playsound
from IPython.display import clear_output
import os
import sys
from platform import system
from afficheur import Afficheur
from scores import Scores

class Demineur():

    def __init__(self, nombreColonnes=5, nombreLignes=10, forcageNombreMines=None,
                 difficulte=10, oldSchool=True, afficheurOldSchoolVisible=False, lifeMode=False, mute=False, DEBUG = False):
        self.__DEBUG__ = DEBUG
        self.system = system()
        self.cheat=False
        self.reset=False
        self.lifeMode=lifeMode
        self.mute=mute
        self.OLD_SCHOOL = oldSchool
        self.NB_LINES=nombreLignes
        self.NB_COLS=nombreColonnes
        self.FORCAGE_MINES=forcageNombreMines
        self.DECALAGE=5
        self.SIDE_W=25*self.NB_COLS+self.DECALAGE*2-1
        self.SIDE_H=25*self.NB_LINES+self.DECALAGE*2-1
        self.nbMinesTrouver=0
        self.coupsPrecedent=[]
        #difficulte de 1 à 20 (4/9/14/19/24/29/34/39/44/49/54/59/64/69/74/79/84/89/94/99% de mines)
        self.difficulte=difficulte
        if(self.FORCAGE_MINES==None):
            self.nbMines=int((self.NB_LINES*self.NB_COLS)*((0.05*(self.difficulte%21))-0.01))
            if (self.nbMines+9) >= (self.NB_LINES*self.NB_COLS):
                self.nbMines-=9
        else:
            if((self.FORCAGE_MINES+9) >= (self.NB_LINES*self.NB_COLS)):
                self.nbMines=(self.NB_LINES*self.NB_COLS)-9
            else:
                self.nbMines=self.FORCAGE_MINES
        self.depart=True
        self.win = False
        self.perdu=False
        self.oneTime = True
        self.score_time_max = sys.maxsize * 2 + 1
        self.score_time = 0
        self.root=Tk()
        self.root.title("Démineur " + str(self.NB_COLS) + "x" + str(self.NB_LINES))
        #Chargement des images:
        self.mine = PhotoImage(file="img/mine.gif")
        self.mine_explosee = PhotoImage(file="img/mine_explosee.gif")
        self.drapeau = PhotoImage(file="img/drapeau.gif")
        self.precedent = PhotoImage(file="img/precedent.gif")
        self.smiley_content = PhotoImage(file="img/smiley_content.gif")
        self.smiley_mort = PhotoImage(file="img/smiley_mort.gif")
        self.aide = PhotoImage(file="img/aide.gif")
        self.son = PhotoImage(file="img/son.gif")
        self.muted = PhotoImage(file="img/mute.gif")
        #Afficheur Temps:
        if self.OLD_SCHOOL:
            self.temps=Afficheur(self.root, column=0, visible=afficheurOldSchoolVisible)
            self.temps.grid(row=0, column=0)
            self.temps.affiche(0)
        else:
            self.temps = Label(text="00:00:00", font=('Helvetica', 24), fg='black')
            self.temps.grid(row=0, column=0)
        #Afficheur Mines:
        if self.OLD_SCHOOL:
            self.mines=Afficheur(self.root, column=2, visible=afficheurOldSchoolVisible)
            self.mines.grid(row=0, column=2)
            self.mines.affiche(self.nbMines)
        else:
            self.mines = Label(text=str(self.nbMinesTrouver)+"/"+str(self.nbMines), font=('Helvetica', 24), fg='black')
            self.mines.grid(row=0, column=2)
        #Boutons precedent, reset, aide et mute:
        self.boutons = Canvas(self.root, width=167, height=41, bg="white")
        self.boutons.create_image((22, 22), image=self.precedent)
        self.boutonSmiley = self.boutons.create_image((64, 22), image=self.smiley_content)
        self.boutons.create_image((106, 22), image=self.aide)
        if self.mute:
            self.boutonMute = self.boutons.create_image((148, 22), image=self.muted)
        else:
            self.boutonSon = self.boutons.create_image((148, 22), image=self.son)
        self.boutons.bind("<Button-1>", self.quelBouton)
        self.boutons.bind("<Button-3>", self.quelBouton)
        self.boutons.grid(row=0, column=1)
        #Plateau du demineur:
        self.cnv=Canvas(self.root, width=self.SIDE_W, height=self.SIDE_H, bg="white")
        #Events:
        self.cnv.bind("<Button-1>", self.clicGauche)
        self.cnv.bind("<Button-3>", self.clicDroit)
        self.root.bind("<Control-Shift-KeyPress-C>", self.leCheatInfernal)
        self.cnv.grid(row=1, column=1)
        #Score:
        self.scores = Scores()
        self.grille=self.generationGrilleVide()
        self.refreshScreen()
        self.root.mainloop()
    
    def leCheatInfernal(self, event):
        if self.depart==True:
            print("CheatInfernal activé! Aucunes mines!")
            self.cheat=True
            self.root.title("Démineur " + str(self.NB_COLS) + "x" + str(self.NB_LINES) + " [CheatInfernal]")
            self.nbMines=0

    def quelBouton(self, event):
        X = (event.x//43)
        if X == 0:
            #Bouton précedent:
            if self.coupsPrecedent != []:
                del self.grille[-1]
                self.grille.append(list(self.coupsPrecedent[-1]))
                del self.coupsPrecedent[-1]
                self.refreshScreen(reset=True)
        elif X == 1:
            #Bouton reset:
            if self.coupsPrecedent != []:
                self.reset=True
                self.win=False
                self.oneTime=True
                self.perdu=False
                self.depart=True
                self.grille = self.generationGrilleVide()
                self.coupsPrecedent=[]
                self.boutons.delete(self.boutonSmiley)
                self.boutonSmiley = self.boutons.create_image((64, 22), image=self.smiley_content)
                self.refreshScreen(reset=True)
        elif X == 2:
            #Bouton aide:
            showinfo("Aide", "Vous disposez d'une grille contenant des mines cachées.\n"+
                             "En cliquant sur une case,\n"+
                             "vous connaissez le nombre de mines se trouvant\n"+
                             "dans les cases (8 au maximum) qui l'entourent.\n"+
                             "Le but du jeu est de détecter toutes les mines sans cliquer dessus.\n"+
                             "Si vous avez deviné la position d'une mine,"+
                             "vous pouvez la faire apparaître par un clic droit sur la case\n"+
                             "(ou en cliquant sur Mine puis sur la case ).")
        elif X == 3:
            #Bouton mute:
            self.mute=not(self.mute)
            if self.mute:
                self.boutons.delete(self.boutonSon)
                self.boutonMute = self.boutons.create_image((148, 22), image=self.muted)
            else:
                self.boutons.delete(self.boutonMute)
                self.boutonSon = self.boutons.create_image((148, 22), image=self.son)
            

    def generationGrilleVide(self):
        G=[]
        Gmines=[]
        for i in range(self.NB_COLS):
            subGrille=[]
            for j in range(self.NB_LINES):
                subGrille.append(False)
            Gmines.append(subGrille)
        G.append(Gmines)
        Gaff=[]
        for i in range(self.NB_COLS):
            subGrille=[]
            for j in range(self.NB_LINES):
                subGrille.append(0)
            Gaff.append(subGrille)
        G.append(Gaff)
        return G
    
    #Indiquer la case par un drapeau/un point d'interrogation/rien:
    def clicDroit(self, event):
        if not(self.win) and not(self.perdu):
            # position du pointeur de la souris
            X = event.x
            Y = event.y
            col, line = self.getCase(X, Y)
            if (self.NB_LINES > line >= 0) and (self.NB_COLS > col >=0):
                #Debug:
                if self.__DEBUG__ :
                    print(X, Y)
                    print(col, line)
                #Rafraichissement de la case choisit:
                if col<len(self.grille[1]) and line<len(self.grille[1][0]):
                    self.changeCase(col, line)
                #Rafraichissement du jeu:
                self.refreshScreen()
                #Debug:
                if self.__DEBUG__ :
                    # on dessine un carré
                    r = 2
                    self.cnv.create_rectangle(X-r, Y-r, X+r, Y+r, outline="black",fill="red")

    #Révéler une case (ou plusieurs):
    def clicGauche(self, event):
        if not(self.win) and not(self.perdu):
            # position du pointeur de la souris
            X = event.x
            Y = event.y
            col, line = self.getCase(X, Y)
            if self.__DEBUG__ :
                print(X, Y)
                print(col, line)
            if (self.NB_LINES > line >= 0) and (self.NB_COLS > col >=0):
                #Mecanique premier tour:
                if self.depart==True:
                    self.firstTour(col, line)
                #Mecanique grille du jeu:
                if col<len(self.grille[1]) and line<len(self.grille[1][0]):
                    self.revelerCase(col, line)
                #Rafraichissement du jeu:
                self.refreshScreen()
                #Debug:
                if self.__DEBUG__ :
                    # on dessine un carré
                    r = 2
                    self.cnv.create_rectangle(X-r, Y-r, X+r, Y+r, outline="black",fill="green")

    def revelerCase(self, x, y):
        if self.grille[1][x][y] == 0:
            if self.grille[0][x][y]:
                self.grille[1][x][y]=4
                self.revelerGrille(x, y)
                self.perdu = True
            else:
                self.grille[1][x][y]=3
                if self.nbMinesAutour(x, y)==0:
                    listeCasesVides = self.detectCasesVidesAutour(x, y, [])
                    while(len(listeCasesVides) > 0):
                        caseVide = listeCasesVides[0]
                        listeCasesVides.remove(caseVide)
                        listeCasesVides = self.detectCasesVidesAutour(caseVide[0], caseVide[1], listeCasesVides)

    def detectCasesVidesAutour(self, x, y, casesVides):
        V = self.voisins(x, y)
        for case in V:
            if self.grille[0][case[0]][case[1]] == False:
                if (self.nbMinesAutour(case[0], case[1]) == 0) and not(self.grille[1][case[0]][case[1]] == 3):
                    casesVides.append(case)
                self.grille[1][case[0]][case[1]]=3
        return casesVides

    def nbMinesAutour(self, x, y):
        V = self.voisins(x, y)
        nbMines=0
        for case in V:
            if self.grille[0][case[0]][case[1]]:
                nbMines+=1
        return nbMines

    #Retourne les cases autours:
    def voisins(self, i, j):
        return [(a, b) for (a, b) in [(i+1, j+1), (i, j+1), (i-1, j+1), (i+1, j), (i-1, j), (i+1, j-1), (i, j-1), (i-1, j-1)]
                if a in range(self.NB_COLS) and b in range(self.NB_LINES)]

    def firstTour(self, X, Y):
        self.grille = self.generationGrille(self.nbMines, X, Y)
        self.grilleDepart = self.grille
        self.start_time = datetime.now().timestamp()
        self.reset=False
        self.depart=False
        self.actualiserTimer()

    def changeCase(self, y, x):
        if 2 >= self.grille[1][y][x] >= 0:
            self.grille[1][y][x]=(self.grille[1][y][x]+1)%3
        return self.grille[1][y][x]

    def getCase(self, x, y):
        return (x-self.DECALAGE)//25, (y-self.DECALAGE)//25

    #fonction revelant les mines si on perd la partie
    def revelerGrille(self, y, x):
        self.boutons.delete(self.boutonSmiley)
        self.boutonSmiley = self.boutons.create_image((64, 22), image=self.smiley_mort)
        if not(self.mute):
            playsound("sounds/explosion.mp3", block = False)
        for i in range(len(self.grille[1])):
            for j in range(len(self.grille[1][0])):
                if not(i==y and j==x) and self.grille[0][i][j]:
                    self.grille[1][i][j]=3

    #fonction revelant les mines si on perd la partie
    def nbMinesDecouvertes(self):
        nbMines=0
        for i in range(len(self.grille[1])):
            for j in range(len(self.grille[1][0])):
                if self.grille[1][i][j]==1:
                    nbMines+=1
        return nbMines

    def generationGrille(self, nbMines, X, Y):
        G=[]
        Gmines=[]
        for i in range(self.NB_COLS):
            subGrille=[]
            for j in range(self.NB_LINES):
                subGrille.append(False)
            Gmines.append(subGrille)
        G.append(Gmines)
        Gaff=[]
        for i in range(self.NB_COLS):
            subGrille=[]
            for j in range(self.NB_LINES):
                subGrille.append(0)
            Gaff.append(subGrille)
        G.append(Gaff)
        whiteList = self.voisins(X, Y)
        whiteList.append((X, Y))
        while(nbMines>0):
            x=randint(0, self.NB_COLS-1)
            y=randint(0, self.NB_LINES-1)
            if not( (x, y) in whiteList):
                if not(G[0][x][y]):
                    G[0][x][y]=True
                    nbMines-=1
        return G
    
    def ajoutCoupPrecedent(self):
        self.coupsPrecedent.append(list(self.grille[1]))

    def refreshScreen(self, reset=False):
        #Suppression des images et rectangles dessines 
        self.cnv.delete("all")
        #Ajout du coup aux coups précédents:
        if not(reset):
            self.ajoutCoupPrecedent()
        #Placement des images
        for line in range(self.NB_LINES):
            for col in range(self.NB_COLS):
                self.cnv.create_rectangle(self.DECALAGE+col*25, self.DECALAGE+line*25, self.DECALAGE+col*25+25, self.DECALAGE+line*25+25, fill='lightgray')
                if self.grille[1][col][line]==1:
                    self.centre=(self.DECALAGE+13+col*25, self.DECALAGE+13+line*25)
                    self.cnv.create_image(self.centre, image=self.drapeau)
                elif self.grille[1][col][line]==2:
                    self.cnv.create_text(self.DECALAGE*3+self.DECALAGE//2+col*25, self.DECALAGE*3+self.DECALAGE//2+line*25,fill="yellow",font="Helvetica 10 bold", text="?")
                elif self.grille[1][col][line]==3 or self.grille[1][col][line]==4:
                    if self.grille[0][col][line]:
                        self.centre=(self.DECALAGE+13+col*25, self.DECALAGE+13+line*25)
                        if self.grille[1][col][line]==4:
                            self.cnv.create_image(self.centre, image=self.mine_explosee)
                        else:
                            self.cnv.create_image(self.centre, image=self.mine)
                    else:
                        self.nbMinesArround = self.nbMinesAutour(col, line)
                        if not(self.nbMinesArround==0):
                            self.cnv.create_text(self.DECALAGE*3+self.DECALAGE//2+col*25, self.DECALAGE*3+self.DECALAGE//2+line*25,fill="darkblue",font="Helvetica 10 bold", text=str(self.nbMinesArround))
                else:
                    self.cnv.create_rectangle(self.DECALAGE+col*25+1, self.DECALAGE+line*25+1, self.DECALAGE+col*25+23, self.DECALAGE+line*25+23, fill='gray')
        #Debug:
        if self.__DEBUG__ :
            if self.system == 'Windows':
                #Clear Windows:
                os.system('cls')
            else:
                #Clear Linux:
                os.system('clear')
            #Clear Jupyter:
            clear_output(wait=True)
            print("Nombre de mines dans le niveau:", self.nbMines, "pour", self.NB_LINES*self.NB_COLS, "cases.")
            print("Type numéro grille:")
            print("0 --> Case vide non-découverte")
            print("1 --> Case vide avec drapeau")
            print("2 --> Case vide avec '?'")
            print("3 --> Case découverte")
            print()
            print("M --> Case avec mine")
            for line in range(self.NB_LINES):
                for col in range(self.NB_COLS):
                    print("--------", end="")
                print("-")
                print("|", end="")
                for col in range(self.NB_COLS):
                    if self.grille[0][col][line]:
                        print(self.grille[1][col][line], "(M)", end="\t")
                    else:
                        print(self.grille[1][col][line], "   ", end="\t")
                print("|")
            for col in range(self.NB_COLS):
                print("--------", end="")
            print("-")

    def checkWin(self):
        self.nbMinesTrouver=0
        nbMinesAvecDrapeaux=0
        casesToutesDecouvertes = True
        for line in range(self.NB_LINES):
            for col in range(self.NB_COLS):
                if self.grille[1][col][line]==0:
                    casesToutesDecouvertes = False
                if self.grille[1][col][line]==1:
                    self.nbMinesTrouver+=1
                    if self.grille[0][col][line]:
                        nbMinesAvecDrapeaux+=1
        return (nbMinesAvecDrapeaux == self.nbMinesTrouver) and casesToutesDecouvertes

    def actualiserTimer(self):
        self.win = self.checkWin()
        if not(self.reset):
            if self.OLD_SCHOOL:
                tmp=self.nbMines-self.nbMinesTrouver
                if tmp<0:
                    tmp=0
                self.mines.affiche(tmp)
            else:
                tmp=self.nbMinesTrouver
                if tmp > self.nbMines:
                    tmp = self.nbMines
                self.mines.configure(text=str(self.nbMinesTrouver)+"/"+str(self.nbMines))
            if not(self.win) and not(self.perdu):
                self.score = int(time() - self.start_time)
                if self.OLD_SCHOOL:
                    self.temps.affiche(self.score)
                else:
                    self.temps.configure(text=strftime("%H:%M:%S", gmtime(self.score)))
            elif self.win and self.oneTime:
                if not(self.mute):
                    playsound("sounds/ta_da.mp3", block = False)
                print("Partie gagné !")
                self.scoreboard=Tk()
                self.scoreboard.title("Scoreboard")
                self.scoreboard.resizable(width=False, height=False)
                self.labelPseudo = Label(self.scoreboard, text='Entrez votre pseudo :')
                self.labelPseudo.grid(row=0, column=0)
                self.entryPseudo = Entry(self.scoreboard, textvariable=StringVar())
                self.entryPseudo.grid(row=1, column=0)
                self.buttonPseudo = Button(self.scoreboard, text='Ok', command=lambda:self.addScore(self.entryPseudo.get()))
                self.buttonPseudo.grid(row=1, column=1)
                self.scoreboard.mainloop()
                self.oneTime = False
            self.root.after(500, self.actualiserTimer)
        else:
            if self.OLD_SCHOOL:
                self.mines.affiche(self.nbMines)
            else:
                self.mines.configure(text=str(0)+"/"+str(self.nbMines))
            if self.OLD_SCHOOL:
                self.temps.affiche(0)
            else:
                self.temps.configure(text=strftime("%H:%M:%S", gmtime(0)))

    def addScore(self, pseudo):
        #Debug:
        if self.__DEBUG__ :
            print("Cheat ?", self.cheat)
            print("Pseudo:", pseudo)
            print("Score:", self.score)
            print("Nombre de mines:", self.nbMines)
            print("Taille grille (X Y):", self.NB_COLS, self.NB_LINES)
        #ajouter le score à la liste:
        if self.cheat:
            self.scores.write(pseudo + " cheateur", self.score, self.NB_COLS, self.NB_LINES, self.nbMines)
        else:
            self.scores.write(pseudo, self.score, self.NB_COLS, self.NB_LINES, self.nbMines)
        self.labelPseudo.destroy()
        self.entryPseudo.destroy()
        self.buttonPseudo.destroy()
        self.scoreboard.destroy()