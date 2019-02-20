#Auteur : Adrien M.

class ResultObject(object):

    #Constructeur
    def __init__(self, name, position, alive, score):

        self.name = name
        self.position = position
        self.alive = alive
        self.score = score
    
    #getters setters
    def getName(self):
        return self.name

    def getPosition(self):
        return self.position

    def getAlive(self):
        return self.alive

    def getScore(self):
        return self.score

    def setName(self, name):
        self.name = name

    def setPosition(self, position):
        self.name = position

    def setAlive(self, alive):
        self.name = alive

    def setScore(self, score):
        self.name = score

    #"""EXEMPLE"""
    #{
    #    "snake1":{
    #      "pos" : [
    #        [1,2],
    #        [1,3],
    #        [1,4],
    #        [1,5],
    #        [1,6]
    #        ],
    #      "alive" : true,
    #      "score" : 654
    #      },
    #    "snake2":{
    #      "pos" : [
    #        [2,2],
    #        [2,3],
    #        ],
    #      "alive" : true,
    #      "score" : 6969
    #    }
    #}

    pass




