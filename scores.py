class Scores():

        def __init__(self, splitter="__SPLITTER__"):
            fichier = open("scores.stats", "a")
            fichier.close()
            self.splitter = splitter
        
        def write(self, pseudo, score, tailleX, tailleY, nbMines):
            fichier = open("scores.stats", "a")
            pseudo = pseudo.replace(self.splitter, "")
            if(pseudo != ""):
                fichier.write(pseudo + "__SPLITTER__" + str(score) + "__SPLITTER__" + str(tailleX) + "x" + str(tailleY) + "__SPLITTER__" + str(nbMines) + "\n")
                fichier.close()
                return True
            fichier.close()
            return False

        def read(self):
            fichier = open("scores.stats", "r")
            string = fichier.read()
            out = []
            for pseudo_score in string.split('\n'):
                liste = pseudo_score.split(self.splitter)
                if(len(liste) == 2):
                    toAppend=[self.decode(liste[0]), self.reverse(liste[1])]
                    if(toAppend[0]!=""):
                        out.append(toAppend)
            fichier.close()
            return out