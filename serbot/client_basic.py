# client_basic.py
import os
import time
import socket
import threading
# from pynput import keyboard

# 소켓 오브젝트 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
host = 'localhost'
port = '10.150.149.152'
client_socket.connect((host, port))

print('Connect to server.')

flagClient = True
while flagClient:
    ch = input()

    # Send data to server
    client_socket.sendall(ch.encode())

    # Receive response from server
    response = client_socket.recv(1024)
    respData = response.decode()
    print('에코:', respData)

    if(ch == 'q'):
        break

# Close the client socket
client_socket.sendall('quit'.encode())
client_socket.close()
print("Thread(socket) finished")