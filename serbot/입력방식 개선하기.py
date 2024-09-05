from pynput import keyboard
# while문 상태를 결정하는 플래그
flagStatus = True

# 키를 눌렀을 때의 동작을 정의하는 함수
def on_press(key):
    global flagStatus
    print(f"Pressed: {key}")
    if key == keyboard.Key.esc or (key.char == 'q'):
        flagStatus = False

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