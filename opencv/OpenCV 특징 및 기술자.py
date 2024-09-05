import cv2
import numpy as np

img1_src = cv2.imread("./images/img_6_6.jpg", cv2.IMREAD_GRAYSCALE)
img1 = cv2.resize(img1_src, (320,240))

keyPoint = cv2.goodFeaturesToTrack(img1, 25, 0.01, 10)
keyPoint = np.int0(keyPoint)

img2 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)

for i in keyPoint:
    x,y = i.ravel()
    cv2.circle(img2, (x,y), 5, (0,0,255))
    cv2.imshow("goodToTrack", img2)

sift = cv2.SIFT.create()
# surf = cv2.xfeatures2d.SURF_create()
fast = cv2.FastFeatureDetector_create()
orb = cv2.ORB_create()

methods = [(sift,'sift'),
           # (surf, 'surf'),
           (fast, 'fast'),
           (orb, 'orb')]

for (method, name) in methods:
    print(name)
    keyPoint = method.detect(img1, None)
    res = cv2.drawKeypoints(img1, keyPoint, img1)
    cv2.imshow(name, res)

cv2.waitKey(0)
cv2.destroyAllWindows()