import numpy as np
import cv2

# 영상 읽기
img1 = cv2.imread('./road.jpg', cv2.IMREAD_GRAYSCALE)

pointx = []
pointy = []
h, w = img1.shape

def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pointx.append(x)
        pointy.append(y)

img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image', mouse_click)

point1_src = np.float32([[pointx[0], pointy[0]], [pointx[1], pointy[1]], [pointx[2], pointy[2]], [pointx[3], pointy[3]]])
point1_dst = np.float32([[pointx[1],pointy[0]], [pointx[1],pointy[1]], [pointx[2],pointy[2]], [pointx[2],pointy[2]]])
per_mat1 = cv2.getPerspectiveTransform(point1_src, point1_dst)
# 투시 변환 수행
res1 = cv2.warpPerspective(img1, per_mat1, (w, h))
cv2.imshow('result', res1)

while True:
    cv2.imshow('image', img1)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
