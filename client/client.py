import socket

#socket
print("- Ready")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("- Socket initialized")
s.connect(("127.0.0.1", 1111))
print("- Socket connected to server")
#socket

import pygame
from pygame.locals import *

pygame.init()

#Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((640, 480),RESIZABLE)

#Chargement et collage du fond
fond = pygame.image.load("C:\\Users\\natha\\OneDrive\\Documents\\GitHub\\Python-CESI\\Pygame test\\hexa.png").convert()
fenetre.blit(fond, (0,0))

#Rafraîchissement de l'écran
pygame.display.flip()

# Start Socket

name = "john"
s.send(name.encode())
r = s.recv(9999999)

print(r)

# End Sockets

#BOUCLE INFINIE
continuer = 1
while continuer:
    for event in pygame.event.get():    #Attente des événements
        if event.type == QUIT:
            continuer = 0

    #Re-collage
    fenetre.blit(fond, (0,0))
    #Rafraichissement
    pygame.display.flip()