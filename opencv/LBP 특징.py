import os
import cv2
import numpy as np

img1_src = cv2.imread("./images/img_6_6.jpg", cv2.IMREAD_GRAYSCALE)
img2_src = cv2.imread("./images/img50.jpg", cv2.IMREAD_GRAYSCALE)
img1 = cv2.resize(img1_src, (320,240))
img2 = cv2.resize(img2_src, (320,240))

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
(hog_peoples, weights) = hog.detectMultiScale(img1, winStride=(8,8), padding=(32,32), scale=1.05)

res1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
for (x,y,w,h) in hog_peoples:
    cv2.rectangle(res1, (x,y), (x + w, y + h), (255,0,0), 2)

cv2.imshow("input1", res1)

cv2.waitKey(0)
cv2.destroyAllWindows()