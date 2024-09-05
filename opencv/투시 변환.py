# 관련 라이브러리 선언
import numpy as np
import cv2
from matplotlib import pyplot as plt

# 영상 읽기
img1 = cv2.imread('./images/img12.jpg', cv2.IMREAD_GRAYSCALE)
img1 = cv2.resize(img1,(320,240))

# 투시 변환 수행
h, w = img1.shape
point1_src = np.float32([[1,1], [w-10,10], [5,h-5],[w-4,h-4]])
point1_dst = np.float32([[15,15], [w-60,15], [10,h-25], [w-100,h-50]])
point2_src = np.float32([[148,145], [168,144], [136,223], [188,222]])
point2_dst = np.float32([[136,145], [188,144], [136,223], [188,222]])
per_mat1 = cv2.getPerspectiveTransform(point1_src, point1_dst)
per_mat2 = cv2.getPerspectiveTransform(point2_src, point2_dst)
res1 = cv2.warpPerspective(img1, per_mat1, (w,h))
res2 = cv2.warpPerspective(img1, per_mat2, (w,h))

# 결과 영상 출력
ress = []
ress.append(img1), ress.append(res1), ress.append(res2)

for i in range(3):
    plt.subplot(2,2,i+1)
    plt.imshow(ress[i], cmap='gray')
    plt.xticks([]), plt.yticks([])
plt.show()
