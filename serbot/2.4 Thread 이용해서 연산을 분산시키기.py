import cv2
import queue
import threading
import numpy as  np

min_Val = 40; max_Val = 1500

threadStat = True
imgSrc = None
imgList = []

imgQ = queue.Queue()

cap = cv2.VideoCapture(0)
ret, imgSrc = cap.read()
if not ret:
    exit()
imgSrc = cv2.cvtColor(imgSrc, cv2.COLOR_BGR2GRAY)
imgQ.put(imgSrc)

width = imgSrc.shape[1]; height = imgSrc.shape[0]
meanX = round(width/2); meanY = round(height/2)

def freeCam(cam, msg):
    cam.release()
    print("\nMain thread finished:", msg)

def getImg(cam):
    ret, frame = cam.read()
    if not ret:
        freeCam(cam, 'read frame error')
    else:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame

def capture_thread():
    global threadStat, cap, meanX, meanY

    while threadStat:
        imgSrc = getImg(cap)
        imgQ.put(imgSrc)

        imgBGR = cv2.cvtColor(imgSrc, cv2.COLOR_GRAY2BGR)
        cv2.circle(imgBGR, (meanX, meanY), 5, (0,0,255), 3)
        cv2.imshow('Processed Frame', imgBGR)
        key = cv2.waitKey(10)

        if(key==ord('q')):
            threadStat = False

    cap.release()
