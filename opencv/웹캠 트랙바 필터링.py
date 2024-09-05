import cv2
import matplotlib as plt

def nothing():
    pass

CAMERA_ID = 0

winName = 'CAM Window'

cam = cv2.VideoCapture(CAMERA_ID)
if cam.isOpened() == False:
    print
    'Cannot open the camera-%d' % (CAMERA_ID)
    exit()

cv2.namedWindow(winName)
cv2.createTrackbar('blur', winName, 0, 255, nothing)
cv2.setTrackbarPos('blur', winName, 1)

while(True):
    ret, frame = cam.read()
    # blur = cv2.getTrackbarPos('blur', winName)
    # res1 = cv2.GaussianBlur(frame, (1,21), blur)
    
    filterSz = cv2.getTrackbarPos('blur', winName)+1
    imgBlur = cv2.boxFilter(frame, -1, (filterSz,filterSz))
    
    cv2.imshow(winName, imgBlur)
    
    if cv2.waitKey(30) & 0xFF == 27:
        break




    
