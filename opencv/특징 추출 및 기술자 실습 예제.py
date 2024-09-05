import numpy as np
import  cv2
import os

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

# 1. Edge detection
image = cv2.imread("namecard.jpg")
orig = image.copy()

cv2.imshow("original", orig)

ratio = 800.0 / image.shape[0]
dim = (int(image.shape[1]*ratio), 800)
image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3,3), 0)
edge = cv2.Canny(gray, 75, 200)

cv2.imshow("edge", edge)

# 2. find dontours
(cnts, _) = cv2.findContours(edge.copy(), cv2.RETR_LIST,
                             cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02*peri, True)

    print(len(approx))

    if len(approx) == 4:
        screenCnt = approx
        break

# 3. apply perspective transform
rect = order_points(screenCnt.reshape(4,2) / ratio)
(topLeft, topRight, bottomRight, bottomLeft) = rect

w1 = abs(bottomRight[0] - bottomLeft[0])
w2 = abs(topRight[0] - topLeft[0])

h2 = abs(topRight[1] - bottomRight[1])
h1 = abs(topRight[1] - bottomRight[0])

maxWidth = int(max([w1, w2]))
maxHeight = int(max([h1, h2]))

dst = np.float32([[0,0], [maxWidth-1,0], [maxWidth-1, maxHeight-1], [0, maxHeight-1]])
M = cv2.getPerspectiveTransform(rect, dst)

warped = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))

# 4. apply adaptive threshold
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
warped = cv2.adaptiveThreshold(warped, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21,10)

cv2.imshow("warped", warped)

cv2.waitKey(0)
cv2.destroyAllWindows()