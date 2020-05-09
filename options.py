from tkinter import *
from tkinter.messagebox import *

class Options():

    def __init__(self):
        fichier = open("options.conf", "a")
        fichier.close()
        self.optionsOpen = False
        
    def menu(self):
        self.optionsOpen = True
        self.fenetreOptions = Tk()
        self.fenetreOptions.title("Options")
        self.fenetreOptions.configure(bg="lightgray")
        self.fenetreOptions.resizable(height = False, width = False)
        self.fenetreOptions.protocol("WM_DELETE_WINDOW", self.onClosing)
        
        liste = self.read()

        Label(self.fenetreOptions, width = 20, anchor=W, bg="lightgray", text = "Compteurs à l'ancienne").grid(row=0, column=0, sticky=W+E+N+S)
        self.cptType = IntVar(self.fenetreOptions)
        Checkbutton(self.fenetreOptions, variable=self.cptType, selectcolor="gray", activebackground = "lightgray", width = 2, indicatoron=0).grid(row=0, column=1, sticky=W+E+N+S)
        if len(liste) > 0:
            self.cptType.set(liste[0])

        Label(self.fenetreOptions, width = 20, anchor=W, bg="lightgray", text = "Segments apparents").grid(row=1, column=0, sticky=W+E+N+S)
        self.segApparents = IntVar(self.fenetreOptions)
        Checkbutton(self.fenetreOptions, variable=self.segApparents, selectcolor="gray", activebackground = "lightgray", indicatoron=0).grid(row=1, column=1, sticky=W+E+N+S)
        if len(liste) > 1:
            self.segApparents.set(liste[1])

        Label(self.fenetreOptions, width = 20, anchor=W, bg="lightgray", text = "Colonnes grille").grid(row=2, column=0, sticky=W+E+N+S)
        self.colonnes = IntVar(self.fenetreOptions, 5)
        self.entColonnes = Entry(self.fenetreOptions, textvariable=self.colonnes, width=3)
        self.entColonnes.grid(row=2, column=1)
        if len(liste) > 2:
            self.colonnes.set(liste[2])

        Label(self.fenetreOptions, width = 20, anchor=W, bg="lightgray", text = "Lignes grille").grid(row=3, column=0, sticky=W+E+N+S)
        self.lignes = IntVar(self.fenetreOptions, 10)
        self.entLignes = Entry(self.fenetreOptions, textvariable=self.lignes, width=3)
        self.entLignes.grid(row=3, column=1)
        if len(liste) > 3:
            self.lignes.set(liste[3])

        Label(self.fenetreOptions, width = 20, anchor=W, bg="lightgray", text = "Difficulté").grid(row=4, column=0, sticky=W+E+N+S)
        self.listDifficulte = [str(i+1) for i in range(20)]
        self.difficulte=StringVar(self.fenetreOptions)
        if len(liste) > 4:
            self.difficulte.set(liste[4])
        else:
            self.difficulte.set(self.listDifficulte[0])
        self.optDifficulte = OptionMenu(self.fenetreOptions, self.difficulte, *self.listDifficulte)
        self.optDifficulte.config(width=2, bg='lightgray',fg='black',
                             activebackground='lightgray',
                             activeforeground='black', highlightthickness=0)
        self.optDifficulte.grid(row=4, column=1, sticky=W+E+N+S)

        Label(self.fenetreOptions, width = 20, anchor=W, bg="lightgray", text = "Nombre de vies de départ\n(LifeMode)").grid(row=5, column=0, sticky=W+E+N+S)
        self.listSelVies = [str(i+1) for i in range(5)]
        self.selVies=StringVar(self.fenetreOptions)
        if len(liste) > 5:
            self.selVies.set(liste[5])
        else:
            self.selVies.set(self.listSelVies[0])
        self.optSelVies = OptionMenu(self.fenetreOptions, self.selVies, *self.listSelVies)
        self.optSelVies.config(width=2, bg='lightgray',fg='black',
                          activebackground='lightgray',
                          activeforeground='black', highlightthickness=0)
        self.optSelVies.grid(row=5, column=1, sticky=W+E+N+S)

        self.validation = Button(self.fenetreOptions, text="Valider", bd=0, font=("Times New Roman", 10, "bold"),
                                       bg='lightgray', activebackground='black',
                                       fg='black', activeforeground='lightgray',
                                       width=12, command=self.valider)
        self.validation.grid(row=6, column=0, sticky=E)

        self.fenetreOptions.mainloop()
    
    def onClosing(self):
        if askokcancel("Quitter", "Voulez-vous quitter\nles options sans les sauvegarder ?"):
            self.optionsOpen=False
            self.fenetreOptions.destroy()

    def valider(self):
        if(self.write()):
            print(self.read())
            self.optionsOpen=False
            self.fenetreOptions.destroy()

    def write(self):
        fichier = open("options.conf", "w")
        if len(self.selVies.get()) > 0:
            sel = str(self.selVies.get())
        else:
            sel = "3"
        if len(self.difficulte.get()) > 0:
            dif = str(self.difficulte.get())
        else:
            dif = "5"
        if self.lignes.get() > 0:
            lines = str(self.lignes.get())
        else:
            lines = "10"
        if self.colonnes.get() > 0:
            col = str(self.colonnes.get())
        else:
            col = "5"
        fichier.write(str(self.cptType.get()) + ";" + str(self.segApparents.get()) + ";" + col + ";" + lines + ";" + dif + ";" + sel)
        fichier.close()
        return True

    def read(self):
        fichier = open("options.conf", "r")
        string = fichier.read()
        fichier.close()
        if string == '':
            return []
        return string.split(';')