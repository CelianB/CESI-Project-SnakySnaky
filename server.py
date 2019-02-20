#Auteur : Nathan W.   / Adrien M.
import socket
import select
import uuid
import sys
import traceback
import json
from resultObject import ResultObject
# Import snake directions
from util.snake_direction import SnakeDirection

from threading import Thread

from util.config_mgmt import ConfigHandler

config_general = ConfigHandler('configs', False, 'config.ini', '')

server_running = True
dicoSocketClients = {}
client_index = 0


def start_server():
	global client_index
	print('Initializing server')
	host = config_general.getStr('ServerIP')
	port = config_general.getInt('ServerPort')

	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket created")
	try:
		soc.bind((host, port))
	except:
		print("Bind failed. Error : " + str(sys.exc_info()))
		sys.exit()

	soc.listen(5) # 5 connections max at the same time
	print('Socket now listening...')

	# Boucle infinie - ne se reset pas à chaques nouveaux clients
	global dicoResultObjet  #dico pour stocker les classes resultObjet (ou snakes) avec l'id client en clef
	
	# Snakes dictionnary
	#initialisation temporairement en dur des serpents
	dicoResultObjet = [1, [ [10,10], [10,11], [10,12], [10,13], [10,14] ] ]
	dicoResultObjet = [2, [ [20,10], [20,11], [20,12], [20,13], [20,14] ] ]
	dicoResultObjet = [3, [ [30,10], [30,11], [30,12], [30,13], [30,14] ] ]
	dicoResultObjet = [4, [ [40,10], [40,11], [40,12], [40,13], [40,14] ] ]
	dicoResultObjet = [5, [ [50,10], [50,11], [50,12], [50,13], [50,14] ] ]


	# Infinite while - Do not reset request
	while server_running:
		dem_connex, wlist, xlist = select.select([soc], [], [], 0.01)
		for connexion in dem_connex:
			recep, infos = connexion.accept()
			client_index += 1
			dicoSocketClients[recep] = client_index
			print('Connected with: ' + str(infos))

		clientsMAJ = []
		try:
			clientsMAJ, wlist, xlist = select.select(dicoSocketClients.keys(), [], [], 0.01)
		except select.error:
			pass
		else:
			try:
				for client in clientsMAJ:
					msg = client.recv(5120)
					msg = json.loads(msg)
					treatMessage(client, msg)
					if len(msg.decode()) > 1:
						print(msg.decode())
			except:
				pass

	soc.close()
	print('Closed')

def treatMessage(connection, msg):
	if msg['type'] == 'move':
		directionEnum = int(msg['direction'])
		process_input(dicoSocketClients[connection], directionEnum)
	elif msg['type'] == 'quit':
		print('Client is requesting to quit')
		connection.close()

# Author : Adrien M.
def process_input(id_client, directionEnum):
	print("Processing the input received from client")
	position = dicoResultObjet[id_client].getPosition()

	#suivi du reste du serpent
	if directionEnum != 0:
		
		i = len(position) - 1

		while i != 0:

			position[i] = position[i-1]
			i-=1

	#déplacement en nouvelle position de tête
	if directionEnum == 1:
		position[0][1] += 1

	if directionEnum == 2:
		position[0][1] -= 1

	if directionEnum == 3:
		position[0][0] -= 1

	if directionEnum == 4:
		position[0][0] += 1

	#dicoResultObjet[id_client].setPosition
	return ResultObject(dicoResultObjet[id_client].name, position, True, dicoResultObjet[id_client].score)


if __name__ == "__main__":
	start_server()