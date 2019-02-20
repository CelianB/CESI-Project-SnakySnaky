import socket
import sys
import traceback

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

    soc.listen(5) # queue up to 5 requests
    print("Socket now listening")

    # infinite loop- do not reset for every requests
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)

        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()
    soc.close()


def client_thread(connection, ip, port, max_buffer_size = 5120):
    is_active = True

    while is_active:
        client_input = receive_input(connection, max_buffer_size)

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
    result = process_input(decoded_input)

    return result


def process_input(id_client, input_enum_int):

    print("Processing the input received from client")    
    position = dicoResultObjet[id_client].getPosition()    

    #suivi du reste du serpent
    if input_enum_int != 0:
        
        imax = len(position) - 1
        i = imax

        while i != 0:

            position[i] = position[i-1]
            i-=1

    #déplacement en nouvelle position de tête
    if input_enum_int == 1:
        position[0][1] += 1

    if input_enum_int == 2:
        position[0][1] -= 1

    if input_enum_int == 3:
        position[0][0] -= 1

    if input_enum_int == 4:
        position[0][0] += 1

    #dicoResultObjet[id_client].setPosition
    myResultObjet(dicoResultObjet[id_client].name, position, True, dicoResultObjet[id_client].score)


if __name__ == "__main__":
    main()