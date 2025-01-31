import cv2 as cv
import os

img = cv.imread('image.jpg')

height = img.shape[0]
width = img.shape[1]

for y in range(0, height):
    # 가로방향 직선(파란선)
    img.itemset(y, int(width/2), 0, 0)    
    img.itemset(y, int(width/2), 1, 0)    
    img.itemset(y, int(width/2), 2, 255)    

for x in range(0, width):
    # 세로방향 직선(빨간선)
    img.itemset(int(height/2), x, 0, 255)  
    img.itemset(int(height/2), x, 1, 0)
    img.itemset(int(height/2), x, 2, 0)    
    
cv.imshow('result',img)
cv.waitKey(0)
cv.destroyAllWindows()