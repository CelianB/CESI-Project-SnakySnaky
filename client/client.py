import socket

print("- Ready")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("- Socket initialized")
s.connect(("127.0.0.1", 1111))
print("- Socket connected to server")

name = "john"

s.send(name.encode())
print("- Socket sent")

r = s.recv(9999999)
print("- Socket finished")

print(r)