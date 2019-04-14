# Auteurs : Celian B. & Nathan W.
from util.config_mgmt import ConfigHandler
import socket
import uuid

class Networking:
#Recuperation des valeurs de configuration du serveur
    config_general = ConfigHandler('configs', False, 'config.ini', '')
    host = config_general.getStr("ServerIP")
    port = config_general.getInt("ServerPort")

    def __init__(self, event_bus):
        self.event_bus = event_bus
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.host, self.port))
            print("- Socket connected to server")
            self.started = True
            self.id = uuid.uuid4().hex

        except:
            self.started = False
            print("Serveur not started")

    def send(self, data):
        if self.started:
            self.s.send(str(data).encode())