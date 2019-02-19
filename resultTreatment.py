class resultTreatment():
    
    """Classe de traitement des demandes client et calcul du résultat"""

    #Constructeur
    def __init__(self, arene, dicoResultObjet, resultObjet):

        self.arene = arene
        self.dicoObjetResult = dicoResultObjet
        self.objetResult = resultObjet


    def calculMoveResult():

        if resultObjet.alive == True:
            try:
                for snake in dicoResultObjet:
                    for p in snake:

                        if resultObjet.pos[0][0] == p[0][0] and resultObjet.pos[0][1] == p[0][1]:
                            resultObjet.alive = False
            except:
                print("Erreur dans le calcul de collisions avec les autres snakes")

        if resultObjet.alive == True :
            try:
                for case in arene:
                    if case[resultObjet.pos[0][0]][resultObjet.pos[0][1]] == 1:
                        resultObjet.alive = False
            except:
                print("Erreur dans le calcul de collisions avec les murs")

pass




