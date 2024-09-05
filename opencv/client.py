# client code
from socket import *

Host = '127.0.0.1'
Port = 9999

client_socket = socket(AF_INET, SOCK_STREAM)

client_socket.connect((Host,Port))
client_socket.sendall('Hi'.encode())

data = client_socket.recv(1024)
print('received from', repr(data.decode()))

client_socket.close()