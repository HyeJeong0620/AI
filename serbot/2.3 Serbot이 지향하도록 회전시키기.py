import time
import cv2
import numpy as np
from pop import Util
from pop import Pilot
from IPython.display import claer_ouput

#######################################################
# 튜닝해볼만한 파라미터
dt_full = 0.08 # 움직임 감지 후 회전하는 시간 (100%)
dt_stop = 0.15 # 움직이고 난 후 정지하는 시간

# 이진화 경계값
thBin = 80

# 움직임 감지를 위한 면적의 기준치
min_Val = 40; max_Val = 500

# 움직이지 않는 범위
deadzone = 0.1
#######################################################
def freeCam(cam, msg):
    cam.release()
    print("\nMain thread finished:",msg)

def getImg(cam):
    ret, frame = cam.read()
    if not ret:
        freeCam(cam, 'read frame error')
    else:
        return frame

def rotation(centerX, width, bot):
    global  gain, dt_full, dt_stop, deadzone

    steering = (centerX - (width/2)) / (width/2)
    bot.steering = steering

    if(steering < -deadzone):
        bot.turnLeft()
    elif(steering > deadzone):
        bot.turnRight()
    else:
        bot.stop()

    dt = float(dt_full * abs(steering))
    time.sleep(dt)

    # 돌리고 나서 일시 정지
    bot.stop()
    time.sleep(dt_stop)

    return steering

########################################################
# vision processing
# try:
    imgTemp = getImg(vid)
    width = imgTemp.shape[1]; height = imgTemp.shape[0]

    # index image 만들기
    row_vector = np.arange(1, width+1)
    img_X = np.tile(row_vector, (height,1))
    img_X = img_X.astype(np.uint16)

    # get background image
    frameBg = getImg(vid)
    meanX = round(width/2); meanY = round(height/2)

    # image subtraction
    for i in range(240):
        frame = getImg(vid)
        imgDiff = cv2.absdiff(frame, frameBg)
        ret, mask = cv2.threshold(imgDiff, 120, 1, cv2.THRESH_BINARY)
        maskCp = cv2.multiply(mask, 255)
        imgBin16 = mask.astype(np.uint16)

        # 256이상의 자퐈를 저장하기 위해서 16비트로 수정
        img_X2 = cv2.multiply(img_X, imgBin16)
        img_X2 = img_X2.astype(np.uint16)

        count = np.count_nonzero(img_X2)
        if count > 300:
            meanX = round(img_X2.sum()/count)

            # steering
            steer = rotation(meanX, width, height)

            print('\rcenter =', meanX,'(', steer, ') ', 'count=', count, end="")

        maskCp = cv2.multiply(mask, 255)
        imgClr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        cv2.circle(imgClr, (meanX, meanY), 5, (0,0,255), 2)
        cv2.imshow("soda", imgClr)

        frameBg = frame
        time.sleep(0.033)

    freeCam(vid, 'no error')

# except:
#    freeCam(vid, 'unknown error')