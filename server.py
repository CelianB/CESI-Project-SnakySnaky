from resultObject import ResultObject
from resultTreatment import ResultTreatment
from assets.map import map_1

import socket, sys
from threading import Thread
import pickle
import random

from util.snake_direction import SnakeDirection
from util.config_mgmt import ConfigHandler

config_general = ConfigHandler('configs', False, 'config.ini', '')

class ThreadClient(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.connexion = conn
        self.resend = True
    
    def treatMessage(self, connexion, msg):
        if msg['type'] == 'move':
            directionEnum = int(msg['direction'])
            # myResultObject = process_input(dicoSocketClients[connexion], directionEnum)
            # myResultTreatment = ResultTreatment(map, dicoResultObject, myResultObject)
        elif msg['type'] == 'start':
            msg_envoi = pickle.dumps({"type" : "start","position" :[random.randint(10,30),random.randint(10,30)],"direction" : random.randint(1,4)})
            connexion.send(msg_envoi)
        elif msg['type'] == 'quit':
            print('Client is requesting to quit')
            connexion.close()

    def run(self):
        nom = self.getName()
        while 1:
            msgClient = self.connexion.recv(1024)
            try:
                msgClient = pickle.loads(msgClient)
                self.treatMessage(self.connexion,msgClient)
            except:
                self.resend = False
            else:
                self.resend = True

            msgEnvoi = pickle.dumps(msgClient)
            if self.resend == True:
                for cle in conn_client:
                    if cle != nom:
                        conn_client[cle].send(msgEnvoi)


        self.connexion.close()
        del conn_client[nom]
        print("Client {} déconnecté.".format(nom))

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    set = config_general.getStr('ServerIP')
    mySocket.bind((config_general.getStr('ServerIP'), config_general.getInt('ServerPort')))
except socket.error:
    print("erreur")
    sys.exit()
print("connecté")
mySocket.listen(5)

conn_client = {}
while 1:
    connexion, adresse = mySocket.accept()
    th = ThreadClient(connexion)
    th.start()
    it = th.getName()
    conn_client[it] = connexion
    print("Client {0} connecté, adresse IP : {1}, port  : {2}".format(it, adresse[0], adresse[1]))


# Author : Adrien M
# def process_input(id_client, directionEnum):
# 	print("Processing the input received from client")
# 	position = dicoResultObject[id_client].getPosition()

# 	# suivi du reste du serpent
# 	if directionEnum != 0:
        
# 		i = len(position) - 1

# 		while i != 0:

# 			position[i] = position[i-1]
# 			i-=1

# 	# déplacement en nouvelle position de tête
# 	if directionEnum == 1:
# 		position[0][1] += 1

# 	if directionEnum == 2:
# 		position[0][1] -= 1

# 	if directionEnum == 3:
# 		position[0][0] -= 1

# 	if directionEnum == 4:
# 		position[0][0] += 1

# 	dicoResultObjet[id_client].setPosition
# 	return ResultObject(dicoResultObject[id_client].name, position, True, dicoResultObject[id_client].score)