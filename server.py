#Auteur : Nathan W.   / Adrien M.
import socket
import select
import uuid
import sys
import traceback
import json
from types import SimpleNamespace as Namespace
import random

from snakeObject import SnakeObject
from assets.map import map_1
from protocolSerialization import ProtocolSerialization
from client.ecs.components import TerrainComponent

# Import snake directions
from util.snake_direction import SnakeDirection


from util.config_mgmt import ConfigHandler

config_general = ConfigHandler('configs', False, 'config.ini', '')
protocolSerialization = ProtocolSerialization()
server_running = True
snakes = []

def start_server():
	print('Initializing server')
	host = config_general.getStr('ServerIP')
	port = config_general.getInt('ServerPort')

	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket created")
	try:
		soc.bind((host, port))
		soc.listen(5)
		print("Le serveur écoute")
	except:
		print("Bind failed. Error : " + str(sys.exc_info()))
		sys.exit()

	connected_clients = []
	while True:
	    # Check es nouvelles connexions éventuelles (toutes les 50ms)
		connexions_request, wlist, xlist = select.select([soc],[], [], 0.05)
		for connexion in connexions_request:
			conn, infos_connexion = connexion.accept()
	        # On ajoute le socket connecté à la liste des clients
			connected_clients.append(conn)
		clients = []
		try:
			clients, wlist, xlist = select.select(connected_clients,[], [], 0.05)
		except select.error:
			pass
		else:
			for client in clients:
				data = client.recv(1024)
				treatMessage(client, data.decode())


def treatMessage(connection, msg):
	msg = json.loads(msg,object_hook=lambda d: Namespace(**d))
	if msg.type == 'move':
		test = snakeUpdate(msg)
		msg_envoi = protocolSerialization.ServerMoveMessage(test)
		connection.send(msg_envoi.encode())
	elif msg.type == 'start':
		msg_envoi = protocolSerialization.ServerStratMessage([random.randint(10,30),random.randint(10,30)],random.randint(1,4))
		connection.send(msg_envoi.encode())
	elif msg.type == 'quit':
		print('Client is requesting to quit')
		connection.close()

def snakeUpdate(msg):
	currentSnake = SnakeObject(msg.id, msg.position, True, 42, msg.direction)
	ind =0
	# Cherche si le snake existe déjà
	for snk in snakes:
		if snk.name == currentSnake.name:
			del snakes[ind]
		ind = ind + 1		
	snakes.append(currentSnake)
	for snake in snakes:
		if(snake.position[0][0] < 2 or snake.position[0][0] > config_general.getInt('MapSize') - 2 
		or snake.position[0][1] < 2 or snake.position[0][1] > config_general.getInt('MapSize') - 2):
			snake.alive = False
	return snakes

if __name__ == "__main__":
	start_server()