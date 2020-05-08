from demineur import Demineur
from options import Options
from scores import Scores
from tkinter import *

class Menu():

    def __init__(self):
        self.opt=Options()
        self.principal = Tk()
        self.principal.title("Démineur Python")
        self.nom=Canvas(self.principal, width=250, height=50, bg='white')
        self.nomText = self.nom.create_text(125,25,fill="black",font=("Gabriola", 30, "bold italic"), text="Démineur")
        mine = PhotoImage(file="img/mine.gif")
        self.nom.create_image((25, 25), image=mine)
        self.nom.create_image((225, 25), image=mine)
        self.nom.grid(row=0, column=0, padx=50)
        self.nom.bind("<Button-1>", self.woaw)
        self.nom.bind("<Button-3>", self.woaw)
        self.principal.bind("<Control-Shift-KeyPress-Y>", self.woaw)
        self.nouvellePartie = Button(self.principal, text="Nouvelle partie", bd=0, font=("Times New Roman", 20, "bold italic"),
                                bg='lightgray', activebackground='gray',
                                fg='gray', activeforeground='lightgray',
                                width=12, command=self.nouvellePartie)
        self.nouvellePartie.grid(row=1, column=0, pady=5)
        self.lifeMode = Button(self.principal, text="LifeMode", bd=0, font=("Times New Roman", 20, "bold italic"),
                               bg='lightgray', activebackground='gray',
                               fg='gray', activeforeground='lightgray',
                               width=12, command=self.lifeMode)
        self.lifeMode.grid(row=2, column=0, pady=5)
        self.scoreboard = Button(self.principal, text="Scoreboard", bd=0, font=("Times New Roman", 20, "bold italic"),
                               bg='lightgray', activebackground='gray',
                               fg='gray', activeforeground='lightgray',
                               width=12, command=self.scoreboard)
        self.scoreboard.grid(row=3, column=0, pady=5)
        self.options = Button(self.principal, text="Options", bd=0, font=("Times New Roman", 20, "bold italic"),
                               bg='lightgray', activebackground='gray',
                               fg='gray', activeforeground='lightgray',
                               width=12, command=self.options)
        self.options.grid(row=4, column=0, pady=5)
        self.principal.mainloop()

    def nouvellePartie(self):
        print(self.opt.optionsOpen == False)
        if self.opt.optionsOpen == False:
            listeVariables=self.readOptions()
            print(listeVariables)
            self.principal.withdraw()
            if len(listeVariables) > 5:
                Demineur(self.principal, nombreColonnes=int(listeVariables[2]), nombreLignes=int(listeVariables[3]), forcageNombreMines=None, difficulte=int(listeVariables[4]), oldSchool=bool(listeVariables[0]), afficheurOldSchoolVisible=bool(listeVariables[1]), lifeMode=None, mute=False, DEBUG = False)
            else:
                Demineur(self.principal, nombreColonnes=5, nombreLignes=10, forcageNombreMines=None, difficulte=4, oldSchool=False, afficheurOldSchoolVisible=False, lifeMode=None, mute=False, DEBUG = False)
        else:
            messagebox.showerror(title="Lancement de partie", message="Veuillez fermer les options avant de lancer une partie.")

    def lifeMode(self):
        print(self.opt.optionsOpen == False)
        if self.opt.optionsOpen == False:
            listeVariables=self.readOptions()
            print(listeVariables)
            self.principal.withdraw()
            if len(listeVariables) > 5:
                Demineur(self.principal, nombreColonnes=int(listeVariables[2]), nombreLignes=int(listeVariables[3]), forcageNombreMines=None, difficulte=int(listeVariables[4]), oldSchool=bool(listeVariables[0]), afficheurOldSchoolVisible=bool(listeVariables[1]), lifeMode=int(listeVariables[5]), mute=False, DEBUG = False)
            else:
                Demineur(self.principal, nombreColonnes=5, nombreLignes=10, forcageNombreMines=None, difficulte=4, oldSchool=False, afficheurOldSchoolVisible=False, lifeMode=3, mute=False, DEBUG = False)
        else:
            messagebox.showerror(title="Lancement de partie", message="Veuillez fermer les options avant de lancer une partie.")
    
    def scoreboard(self):
        self.scores = Scores()
        self.principal.withdraw()
        self.scoreboardWindow=Toplevel(self.principal)
        self.scoreboardWindow.protocol("WM_DELETE_WINDOW", self.onClosingScoreboardWindow)
        self.boutonNormalMode = Button(self.scoreboardWindow, text="Mode normal", bd=0, font=("Times New Roman", 10, "bold italic"),
                               bg='lightgray', activebackground='gray',
                               fg='gray', activeforeground='lightgray',
                               width=10, command=self.refreshListeScoresNormal)
        self.boutonNormalMode.grid(row=0, column=0)
        self.boutonLifeMode = Button(self.scoreboardWindow, text="Life Mode", bd=0, font=("Times New Roman", 10, "bold italic"),
                               bg='lightgray', activebackground='gray',
                               fg='gray', activeforeground='lightgray',
                               width=10, command=self.refreshListeScoresLifeMode)
        self.boutonLifeMode.grid(row=1, column=0)
        self.boutonRetour = Button(self.scoreboardWindow, text="Retour", bd=0, font=("Times New Roman", 10, "bold italic"),
                               bg='lightgray', activebackground='gray',
                               fg='gray', activeforeground='lightgray',
                               width=10, command=self.onClosingScoreboardWindow)
        self.boutonRetour.grid(row=2, column=0)
        self.entete = Canvas(self.scoreboardWindow, width=350, height=20)
        self.entete.grid(row=0, column=1)
        self.listeScores = Canvas(self.scoreboardWindow, width=350, height=100, scrollregion=(0, 0, 0, 20))
        self.listeScores.grid(row=1, column=1)
        self.defilY = Scrollbar(self.scoreboardWindow, orient='vertical', command=self.listeScores.yview)
        self.defilY.grid(row=1, column=2, sticky='ns')
        self.listeScores['yscrollcommand'] = self.defilY.set
        self.refreshListeScoresNormal()
    
    def refreshListeScoresNormal(self):
        self.entete.destroy()
        self.entete = Canvas(self.scoreboardWindow, width=350, height=20)
        self.entete.grid(row=0, column=1)
        self.entete.create_text( 75,10,fill="black",font=("Times New Roman", 10, "bold"), text="Pseudo")
        self.entete.create_text(175,10,fill="black",font=("Times New Roman", 10, "bold"), text="Score")
        self.entete.create_text(225,10,fill="black",font=("Times New Roman", 10, "bold"), text="Taille")
        self.entete.create_text(300,10,fill="black",font=("Times New Roman", 10, "bold"), text="Nombre de mines")
        liste = self.scores.read(lifemode=False)
        print("=========[Scoreboard]=========")
        for score in liste:
            print(score)
        print("==============================")
        self.listeScores.destroy()
        self.listeScores = Canvas(self.scoreboardWindow, width=350, height=100, scrollregion=(0, 0, 0, len(liste)*20))
        self.defilY.destroy()
        self.defilY = Scrollbar(self.scoreboardWindow, orient='vertical', command=self.listeScores.yview)
        self.defilY.grid(row=1, column=2, sticky='ns')
        self.listeScores['yscrollcommand'] = self.defilY.set
        self.listeScores.grid(row=1, column=1)
        i=0
        for score in liste:
            self.listeScores.create_text( 75,10+20*i,fill="black",font=("Times New Roman", 10, "bold"), text=score[0])
            self.listeScores.create_text(175,10+20*i,fill="black",font=("Times New Roman", 10, "bold"), text=score[1])
            self.listeScores.create_text(225,10+20*i,fill="black",font=("Times New Roman", 10, "bold"), text=score[2])
            self.listeScores.create_text(300,10+20*i,fill="black",font=("Times New Roman", 10, "bold"), text=score[3])
            i+=1

    def refreshListeScoresLifeMode(self):
        self.entete.destroy()
        self.entete = Canvas(self.scoreboardWindow, width=250, height=20)
        self.entete.grid(row=0, column=1)
        self.entete.create_text( 75,10,fill="black",font=("Times New Roman", 10, "bold"), text="Pseudo")
        self.entete.create_text(200,10,fill="black",font=("Times New Roman", 10, "bold"), text="Victoire(s)")
        liste = self.scores.read(lifemode=True)
        print("====[Scoreboard  LifeMode]====")
        for score in liste:
            print(score)
        print("==============================")
        self.listeScores.destroy()
        self.listeScores = Canvas(self.scoreboardWindow, width=250, height=100, scrollregion=(0, 0, 0, len(liste)*20))
        self.defilY.destroy()
        self.defilY = Scrollbar(self.scoreboardWindow, orient='vertical', command=self.listeScores.yview)
        self.defilY.grid(row=1, column=2, sticky='ns')
        self.listeScores['yscrollcommand'] = self.defilY.set
        self.listeScores.grid(row=1, column=1)
        i=0
        for score in liste:
            self.listeScores.create_text( 75,10+20*i,fill="black",font=("Times New Roman", 10, "bold"), text=score[0])
            self.listeScores.create_text(200,10+20*i,fill="black",font=("Times New Roman", 10, "bold"), text=score[1])
            i+=1

    def onClosingScoreboardWindow(self):
        self.scoreboardWindow.destroy()
        self.principal.deiconify()

    def onClosing(self):
        if askokcancel("Quitter", "Voulez-vous quitter le jeu ?"):
            self.principal.destroy()

    def options(self):
        self.opt.menu()
        
    def readOptions(self):
        fichier = open("options.conf", "r")
        string = fichier.read()
        fichier.close()
        if string == '':
            return []
        return string.split(';')

    def woaw(self, event):
        if self.nom["background"] == "black":
            self.nom.configure(bg='white')
            self.nom.delete(self.nomText)
            self.nomText = self.nom.create_text(75,25,fill="black",font=("Gabriola", 30, "bold italic"), text="Démineur")
        else:
            self.nom.configure(bg='black')
            self.nom.delete(self.nomText)
            self.nomText = self.nom.create_text(75,25,fill="white",font=("Gabriola", 30, "bold italic"), text="Démineur")