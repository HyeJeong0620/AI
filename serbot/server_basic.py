# server_basic.py
import socket

# 소켓 오브젝트 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
host = 'localhost'
port = '10.150.149.152'
server_socket.bind((host, port)) # tuple (host, port) 주의

# Listen 모드 대기
server_socket.listen(1)
print('Server started. Waiting for connections...')

flagServer = True
while flagServer:
    # 클라이언트의 연결 시도를 수락함
    client_socket, address = server_socket.accept()
    print('Connected by', address)

    while True:
        # 클라이언트로부터 데이터를 받음(1024바이트)
        data = client_socket.recv(1024)
        # data가 비어있다면 empty로 생각함
        if not data:
            break

        rcvData = data.decode()
        if not (rcvData == 'quit'):
            flagServer = False
            print('수신:', rcvData.encode())
        else:
            print('종료:', rcvData.encode())
            break

        # Send response back to client
        client_socket.sendall(data)

    # Close the client socket
    client_socket.close()