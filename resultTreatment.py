#Auteur : Adrien M.

class resultTreatment():
    
    """Classe de traitement des demandes client et calcul du résultat"""

    #Constructeur
    def __init__(self, arene, dicoResultObjet, myResultObjet):

        self.arene = arene
        self.dicoResultObjet = dicoResultObjet
        self.myResultObjet = myResultObjet


    def calculMoveResult():

        #vérification que le mouvement est autorisé (un serpent ne se mord pas la queue !)
        #=> traité comme les autres collisions actuellement ; ci-dessous car le snake fait partie du dico

        #recherche de collision avec d'autre snake
        if myResultObjet.alive == True:
            try:
                for snake in dicoResultObjet:
                    for p in snake:

                        if myResultObjet.pos[0][0] == p[0][0] and myResultObjet.pos[0][1] == p[0][1]:
                            myResultObjet.alive = False
            except:
                print("Erreur : calcul de collisions avec les autres snakes")

        #recherche de collision avec un mur
        if myResultObjet.alive == True :
            try:
                for case in arene:
                    if case[myResultObjet.pos[0][0]][myResultObjet.pos[0][1]] == 1:
                        myResultObjet.alive = False
            except:
                print("Erreur : calcul de collisions avec les murs")

    def memoriseMove(indexResultObjet):

        if myResultObjet.alive == True:
            try:
                dicoObjetResult[indexResultObjet] = myResultObjet

            except:
                print("Erreur : mémorisation du nouveau positionnement")
pass




