#Auteur : Adrien M.

class ResultTreatment():
    
    """Classe de traitement des demandes client et calcul du résultat"""

    #Constructeur
    def __init__(self, arene, dicoResultObjet, myResultObjet):

        self.arene = arene
        self.dicoResultObjet = dicoResultObjet
        self.myResultObjet = myResultObjet

    #Traitement du mouvement du joueur
    def calculMoveResult(self):

        #vérification que le mouvement est autorisé (un serpent ne se mord pas la queue !)
        #=> traité comme les autres collisions actuellement ; ci-dessous car le snake fait partie du dico

        #recherche de collision avec d'autre snake
        if self.myResultObjet.alive == True:
            try:
                for snake in self.dicoResultObjet:
                    for p in snake:

                        if self.myResultObjet.pos[0][0] == p[0][0] and self.myResultObjet.pos[0][1] == p[0][1]:
                            self.myResultObjet.alive = False
            except:
                print("Erreur : calcul de collisions avec les autres snakes")

        #recherche de collision avec un mur
        if self.myResultObjet.alive == True :
            try:
                for case in self.arene:
                    if case[self.myResultObjet.pos[0][0]][self.myResultObjet.pos[0][1]] == 'X':
                        self.myResultObjet.alive = False
            except:
                print("Erreur : calcul de collisions avec les murs")

    #Memorisation du nouveau positionnement
    def memoriseMove(self, indexResultObjet):

        if self.myResultObjet.alive == True:
            try:
                self.dicoObjetResult[indexResultObjet] = self.myResultObjet

            except:
                print("Erreur : mémorisation du nouveau positionnement")
pass




