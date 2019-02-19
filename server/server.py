import socket
import threading
import sys
import os

cwd = os.getcwd() + "/util/"
sys.path.append(cwd)

from util.config import ConfigHandler

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))

    def run(self): 
    
        print("Connexion de %s %s" % (self.ip, self.port, ))

        r = self.clientsocket.recv(2048)
        print("User input: ", r)
        message = "Lu par le serveur"
        self.clientsocket.send(message.encode())

        print("Client déconnecté...")


config_general = ConfigHandler('configs', False, 'config.ini', '')

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((config_general.getStr("ServerIP"),config_general.getStr("ServerPort")))

while True:
    tcpsock.listen(10)
    print( "En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()