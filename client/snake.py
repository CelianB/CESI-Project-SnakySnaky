import pygame
import os

class Snake:
    parentPath = os.path.dirname(os.path.dirname(__file__))
    assetsPath = os.path.join(parentPath, 'assets') 
    texturesPath = os.path.join(assetsPath, 'textures')

    
    # exemple
    position = [
        [25,25],[26,25],[27,25],[28,25],[29,25],[30,25],[31,25]
    ]

    sprites = {
        "corner_left_top" :  pygame.image.load(os.path.join(texturesPath, 'corner_left_top.png')),
        "corner_right_top" : pygame.image.load(os.path.join(texturesPath, 'corner_right_top.png')),
        "half_turn" : pygame.image.load(os.path.join(texturesPath, 'half_turn.png')),
        "head" : pygame.image.load(os.path.join(texturesPath, 'head.png')),
        "tail" : pygame.image.load(os.path.join(texturesPath, 'tail.png')),
        "mini_snake" : pygame.image.load(os.path.join(texturesPath, 'mini_snake.png')),
        "straight" : pygame.image.load(os.path.join(texturesPath, 'straight.png')),
    }
    direction = 3
        
    def moveRight(self):
        self.direction = 1
 
    def moveLeft(self):
        self.direction = 3
 
    def moveUp(self):
        self.direction = 0
 
    def moveDown(self):
        self.direction = 2 
    
    def getHeadRotation(self):
        if self.direction == 0:
            return 0
        elif self.direction == 1:
            return 270
        elif self.direction == 2:
            return 180
        elif self.direction == 3:
            return 90
    
    def getRotation(self,beforeCase,currentCase):
        if(beforeCase[0]>currentCase[0]):
            return 270
        elif (beforeCase[0]<currentCase[0]):
            return 90
        elif (beforeCase[1]>currentCase[1]):
            return 180
        elif (beforeCase[1]<currentCase[1]):
            return 0

    def draw(self,surface):
        for i,pos in enumerate(self.position):
            if i == 0:
                img = "head" if (len(self.position) != 1) else "mini_snake"
                r = self.getHeadRotation()
            else:
                r = self.getRotation(self.position[i-1],self.position[i])
                if i == len(self.position):
                    img = "tail"
                else:
                    img = "straight"
            surface.blit(pygame.transform.rotate(self.sprites[img],r),(pos[0] * 16, pos[1] * 16))

    def addLength(self):
        # On récupère la valeur de première "tête" et on définit ça futur position en fonction de la direction
        newpos = self.position[0][:]

        if self.direction==0:
            newpos[1]-=1
        elif self.direction==1:
            newpos[0]+=1
        elif self.direction==2:
            newpos[1]+=1
        elif self.direction==3:
            newpos[0]-=1

        # On met la nouvelle case en première position du tableau
        self.position.insert(0,newpos)

    def removeLast(self):
        # On supprime le dernier element
        self.position.pop()

    def update(self):
        self.addLength()
        self.removeLast()
    

