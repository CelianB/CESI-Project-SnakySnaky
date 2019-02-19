class resultTreatment():
    
    """Classe de traitement des demandes client et calcul du résultat"""

    #Constructeur
    def __init__(self, arene, dicoResultObjet, resultObjet):

        self.arene = arene
        self.dicoObjetResult = dicoResultObjet
        self.objetResult = resultObjet


    def calculMoveResult():

        #vérification que le mouvement est autorisé (un serpent ne se mord pas la queue !)
        #=> traité comme les autres collisions actuellement ; ci-dessous car le snake fait partie du dico

        #recherche de collision avec d'autre snake
        if resultObjet.alive == True:
            try:
                for snake in dicoResultObjet:
                    for p in snake:

                        if resultObjet.pos[0][0] == p[0][0] and resultObjet.pos[0][1] == p[0][1]:
                            resultObjet.alive = False
            except:
                print("Erreur : calcul de collisions avec les autres snakes")

        #recherche de collision avec un mur
        if resultObjet.alive == True :
            try:
                for case in arene:
                    if case[resultObjet.pos[0][0]][resultObjet.pos[0][1]] == 1:
                        resultObjet.alive = False
            except:
                print("Erreur : calcul de collisions avec les murs")

    def memoriseMove(indexResultObjet):

        if resultObjet.alive == True:
            try:
                dicoObjetResult[indexResultObjet] = resultObjet

            except:
                print("Erreur : mémorisation du nouveau positionnement")
pass




