import cv2

CAMERA_ID = 0
flag = False
flag2 = False

cam = cv2.VideoCapture(CAMERA_ID)
if not cam.isOpened():
    print('Cannot open the camera-%d' % CAMERA_ID)
    exit()

winName = 'CAM Window'
cv2.namedWindow(winName)

while True:
    ret, frame = cam.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    key = cv2.waitKey(1)

    if key & 0xFF == ord('q'):
        break

    if key & 0xFF == ord('a'):
        bg = gray_frame.copy()
        flag = True

    if flag:
        # 차영상 모드
        abs = cv2.absdiff(gray_frame, bg)
        cv2.imshow(winName, abs)
    else:
        # 오리지널 모드
        cv2.imshow(winName, gray_frame)

    if key & 0xFF == ord('b'):
        bg = gray_frame.copy()
        flag2 = True

    if flag2:
        ret, thr = cv2.threshold(abs, 60, 255, cv2.THRESH_BINARY)
        cv2.imshow(winName, thr)

cam.release()
cv2.destroyAllWindows()
