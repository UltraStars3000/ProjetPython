#! usr/bin/python

from tkinter import *

class Afficheur(Frame):
        code={1:(2,3),2:(1,2,7,5,4),3:(1,2,7,3,4),4:(6,7,2,3),5:(1,6,7,3,4),6:(1,6,5,4,3,7),
              7:(1,2,3),8:(1,2,3,4,5,6,7),9:(6,1,2,3,4,7),0:(1,2,3,4,5,6)}

        def __init__(self, tk, column, size=1, nCadrans=3, visible=False):
            Frame.__init__(self)
            if nCadrans < 1:
                nCadrans = 1
            self.dic={1: ( 8*size,  7*size, 23*size,  4*size), 2: (22*size,  7*size, 25*size, 19*size),
                      3: (22*size, 22*size, 25*size, 37*size), 4: (23*size, 36*size,  8*size, 39*size),
                      5: ( 5*size, 37*size,  8*size, 22*size), 6: ( 8*size, 19*size,  5*size,  7*size),
                      7: ( 8*size, 19*size, 23*size, 22*size)}
            self.configure(bg="grey40",bd=0,relief=FLAT)
            self.master.resizable(width=False, height=False)
            self.lst=[]
            self.visible=visible
            self.build(tk, size, column, nCadrans)

        def build(self, tk, size, c, n):
            self.can=Canvas(tk,bg='black',relief=FLAT,width =25*size*n,height =42*size, bd=0, highlightthickness=0)
            self.can.grid(row=0,column=c)
            for j in range(n):
                for i in [1,2,3,4,5,6,7]:#Mise en place des segments de l'afficheur
                    liste=[]
                    v=self.dic[i]
                    liste.append(v)
                    for (w,x,y,z) in liste:
                        if(self.visible):
                            p=self.can.create_rectangle(w+(25*j),x,y+(25*j),z,fill='grey40')
                        else:
                            p=self.can.create_rectangle(w+(25*j),x,y+(25*j),z,fill='black')
                        self.lst.append(p)
            #self.initialisation()

        def quitter(self,event=None):
                self.can.delete(ALL)
                self.destroy()

        def affiche(self,arg=None):
            self.initialisation()
            if(arg != None):
                nbr_separes = [int(nbr) for nbr in str(arg) if nbr in '0123456789']
                cpt = len(self.lst)//8
                for j in range(len(nbr_separes)-1, -1, -1):
                    v=list(self.code[nbr_separes[j]])
                    for i in v:
                        self.can.itemconfig(i+(cpt*7),fill='red')
                    cpt-=1
                if(len(nbr_separes)-1 < len(self.lst)//8):
                    while cpt >= 0:
                        v=list(self.code[0])
                        for i in v:
                            self.can.itemconfig(i+(cpt*7),fill='red')
                        cpt-=1

        def initialisation(self):
            for i in self.lst:
                if(self.visible):
                    self.can.itemconfig(i,fill='grey40')
                else:
                    self.can.itemconfig(i,fill='black')