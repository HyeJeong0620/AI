import numpy as np
import cv2
from matplotlib import pyplot as plt

# 영상 읽기
img1_src = cv2.imread("./images/img_6_4.png", cv2.IMREAD_GRAYSCALE)
img1 = cv2.resize(img1_src,(320,240))

# 코너 감지
dst = cv2.cornerHarris(img1, 2,3, 0.06)
dst = cv2.dilate(dst, None)
res1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
res1[dst>0.1*dst.max()] = [0,0,255]

# 결과 영상 출력
displays = [("input", img1), ("res1", res1)]
for (name, out) in displays:
    cv2.imshow(name,out)

# 키보드 입력을 기다린 후 모든 영상창 닫기
cv2.waitKey(0)
cv2.destroyAllWindows()