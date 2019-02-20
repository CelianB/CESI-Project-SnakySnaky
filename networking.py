
from util.config_mgmt import ConfigHandler
import socket

class Networking:
#Recuperation des valeurs de configuration du serveur
    config_general = ConfigHandler('configs', False, 'config.ini', '')
    host = config_general.getStr("ServerIP")
    port = config_general.getInt("ServerPort")

    def __init__(self):
        #Debut Connecxion au serveur
        print("- Ready")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("- Socket initialized")
        self.s.connect((self.host, self.port))
        print("- Socket connected to server")
        #Fin de connexion au serveur

    def send(self, data):
        self.s.send(data)