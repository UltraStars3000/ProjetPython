class Scores():

        def __init__(self, splitter="__SPLITTER__"):
            fichier = open("scores.stats", "a")
            fichier.close()
            self.splitter = splitter
        
        def write(self, pseudo, nbMines, score=0, tailleX=0, tailleY=0, lifeMode=None):
            if lifeMode != None:
                fichier = open("scores_lifemode.stats", "a")
                pseudo = pseudo.replace(self.splitter, "")
                if(pseudo != ""):
                    fichier.write(pseudo + "__SPLITTER__" + str(lifeMode) + "\n")
                    fichier.close()
                    return True
                fichier.close()
            else:
                fichier = open("scores.stats", "a")
                pseudo = pseudo.replace(self.splitter, "")
                if(pseudo != ""):
                    fichier.write(pseudo + "__SPLITTER__" + str(score) + "__SPLITTER__" + str(tailleX) + "x" + str(tailleY) + "__SPLITTER__" + str(nbMines) + "\n")
                    fichier.close()
                    return True
                fichier.close()
            return False

        def read(self, lifemode=False):
            if lifemode:
                fichier = open("scores_lifemode.stats", "r")
                string = fichier.read()
                out = []
                for pseudo_score in string.split('\n'):
                    liste = pseudo_score.split(self.splitter)
                    if(len(liste) == 2):
                        toAppend=[liste[0], liste[1]] #pseudo ; nombre de parties effectuées (lifetime)
                        if(toAppend[0]!=""):
                            out.append(toAppend)
                fichier.close()
            else:
                fichier = open("scores.stats", "r")
                string = fichier.read()
                out = []
                for pseudo_score in string.split('\n'):
                    liste = pseudo_score.split(self.splitter)
                    if(len(liste) == 4):
                        toAppend=[liste[0], liste[1], liste[2], liste[3]] #pseudo ; score ; tailleX x tailleY ; nbMines
                        if(toAppend[0]!=""):
                            out.append(toAppend)
                fichier.close()
            return out