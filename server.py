# Nathan
# Adrien
import socket
import sys
import traceback
import json
from resultObject import ResultObject

from threading import Thread

from util.config_mgmt import ConfigHandler

config_general = ConfigHandler('configs', False, 'config.ini', '')

def main():
    start_server()


def start_server():
    # host = "127.0.0.1"
    # port =1111
    host = config_general.getStr("ServerIP")
    port = config_general.getInt("ServerPort")

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created")
    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(5) # Maximum de 5 utilisateurs
    print("Socket now listening")

    # Boucle infinie - ne se reset pas à chaques nouveaux clients
    global dicoSocketClients
    dicoSocketClients = {}    
    id = 1

    global dicoResultObjet  #dico pour stocker les classes resultObjet (ou snakes) avec l'id client en clef
    
    #initialisation temporairement en dur des serpents
    dicoResultObjet = [1, [ [10,10], [10,11], [10,12], [10,13], [10,14] ] ]
    dicoResultObjet = [2, [ [20,10], [20,11], [20,12], [20,13], [20,14] ] ]
    dicoResultObjet = [3, [ [30,10], [30,11], [30,12], [30,13], [30,14] ] ]
    dicoResultObjet = [4, [ [40,10], [40,11], [40,12], [40,13], [40,14] ] ]
    dicoResultObjet = [5, [ [50,10], [50,11], [50,12], [50,13], [50,14] ] ]


    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)
        
        dicoSocketClients = [connection, id]
        id += 1

        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()            
        except:
            print("Thread did not start.")
            traceback.print_exc()
    soc.close()


def client_thread(connection, ip, port, max_buffer_size = 5120):
    is_active = True

    while is_active:
        myResultObjet = receive_input(connection, max_buffer_size)

        if "--QUIT--" in client_input:
            print("Client is requesting to quit")
            connection.close()
            print("Connection " + ip + ":" + port + " closed")
            is_active = False
        else:
            print("Processed result: {}".format(client_input))
            connection.sendall("-".encode("utf8"))


def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)

    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    
    id_client = dicoSocketClients.get(connection)
    myResultObjet = decode_transmission(decoded_input, id_client)

    return myResultObjet


def decode_transmission(decoded_input, id_client):
   
#Auteur : Adrien M.    

    deserialized_object = json.loads(decoded_input)
    directionEnum = int(deserialized_object['direction'])

# EXEMPLE --
#    {
#  "direction" : 2
#}

    return process_input(id_client, directionEnum)


def process_input(id_client, directionEnum):

#Auteur : Adrien M.
    
    print("Processing the input received from client")    
    position = dicoResultObjet[id_client].getPosition()    

    #suivi du reste du serpent
    if directionEnum != 0:
        
        imax = len(position) - 1
        i = imax

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
    main()