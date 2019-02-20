# Auteurs : Celian B. & Nathan W.
from util.config_mgmt import ConfigHandler
import socket

class Networking:
#Recuperation des valeurs de configuration du serveur
    config_general = ConfigHandler('configs', False, 'config.ini', '')
    host = config_general.getStr("ServerIP")
    port = config_general.getInt("ServerPort")

    def __init__(self, event_bus):
        self.event_bus = event_bus
        try:
            #Debut Connecxion au serveur
            print("- Ready")
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("- Socket initialized")
            self.s.connect((self.host, self.port))
            print("- Socket connected to server")
            #Fin de connexion au serveur
            self.started = True
        except:
            self.started = False
            print("Serveur not started")

    def send(self, data):
        if self.started:
            print("Sent date" + str(data))
            self.s.send(str(data).encode())