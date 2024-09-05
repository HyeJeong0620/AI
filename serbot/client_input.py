# client_input.py
import os
import socket
from pynput import keyboard

# 키를 눌렀을 때의 동작을 정의하는 함수
def on_press(key):
    global flagStatus, client_socket

    print(f"Pressed: {key}")
    if key == keyboard.Key.esc or (key.char == 'q'):
        flagStatus = False
    else:
        # Send data to server
        client_socket.sendall(key.char.encode())
        # Receive response from server
        response = client_socket.recv(1024)
        respData = response.decode()
        print('echo:', respData)

# 소켓 오브젝트 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
host = 'localhost'
port = 12345
client_socket.connect((host, port))

print('Connect to server.')

# while문 상태를 결정하는 플래그
flagStatus = True

# 키보드 이벤트 리스너 생성
listener = keyboard.Listener(on_press=on_press)

# 키보드 이벤트 리스너 실행
listener.start()

# ESC 혹은 'Ctrl+C'를 누르기 전까지 계속 실행
try:
    while flagStatus:
        pass
except KeyboardInterrupt:
    # Stop the listener
    listener.stop()

# Close the client socket
client_socket.sendall('quit'.encode())
client_socket.close()
print("Thread(socket) finished")