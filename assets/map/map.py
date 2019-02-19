#lire un fichier
import os
from array import *

m = 60
n = 60
a = [[0] * m] * n

x = 0
y = 0

with open(os.path.join(os.getcwd(),"assets/map/map.txt"), "r") as contenu:
    for line in contenu:
        for character in line:
            print("y = ", y)
            a[x][y] = character
            y+=1
        y = 0
        x+=1
        print("x = ", x)