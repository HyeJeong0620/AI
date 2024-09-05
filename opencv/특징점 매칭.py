import cv2
import numpy as np

mouseDrawing = False
startX, startY, endX, endY = -1, -1, -1, -1
minMatchCount = 1
viewName = 'input image'

# 특징 선언
sift = cv2.xfeatures2d.SIFT_create()
brisk = cv2.BRISK.create()
orb = cv2.ORB_create()

#-------------------------------
# Brute-Force 기반 매칭
def BruteForce(img1, img2):
    methods = [(sift, cv2.NORM_L2, 'bf_sift'),
               (brisk, cv2.NORM_L2, 'bf_sift'),
               (orb, cv2.NORM_L2, 'bf_sift'),]
    flag = cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS

    for (method, dist, name) in methods:
        keyP1, des1 = method.detectAndCompute(img1, None)
        keyP2, des2 = method.detectAndCompute(img2, None)

        # Brute Force 선언 및 매칭 수행
        bf = cv2.BFMatcher_create(dist, True)
        mat = bf.match(des1, des2)
        mat = sorted(mat, key=lambda x:x.distance)
        res = cv2.drawMatches(img1, keyP1, img2, keyP2, mat[0:20], None, flags=flag)

        bfKnn = cv2.BFMatcher()
        matKnn = bfKnn.knnMatch(des1, des2, k = 2)
        # 매칭 결과 선별
        good = []
        for m, n in matKnn:
            if m.distance < 0.75 * n.distance:
                good.append(m)
        # 기하학적 관계 기반의 매칭 결과 선별
        if len(good) >= minMatchCount:
            img1KP = np.float32([keyP1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            img2KP = np.float32([keyP2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            _m, mask = cv2.findHomography(img1KP, img2KP, cv2.RANSAC, 5.0)
            ransacMask = mask.revel().tolist()
            drawParams = dict(matchColor=(0,255,0),
                              singlePointColor=(0,0,255),
                              matchesMask=ransacMask[0:20],
                              flags=flag)

            resKnn = cv2.drawMatchesKnn(img1,keyP1,img2,keyP2,[good[0:20]],None,flags=flag)
            resKnn2 = cv2.drawMatches(img1,keyP1,img2,keyP2,good[0:20],None,**drawParams)

            cv2.imshow(name+"Knn", resKnn)
            cv2.imshow(name+"KnnRansac", resKnn2)

#------------------------------------------------------------------
#--- FLANN 기반 매칭
def flann(img1, img2):
    # flann 변수 설정
    flannIndexKdtree = 1
    indexParmasKdtree = dict(algorithm=flannIndexKdtree, tress=5)
    searchParms = dict(checks=50)
    flannKdtree = cv2.FlannBasedMatcher(indexParmasKdtree, searchParms)

    flannIndexLsh = 6
    indexParmasLsh = dict(algorithm=flannIndexLsh,
                          table_number=6,
                          key_size=12,
                          multi_probe_level=1)
    flannLsh = cv2.FlannBasedMatcher(indexParmasLsh, searchParms)

    methods = [(sift, flannKdtree, 'flann_sift'),
               (brisk, flannLsh, 'flann_brisk'),
               (orb, flannLsh, 'flann_orb')]

    # 매칭 수행
    for (method, matcher, name) in methods:
        keyP1, des1 = method.detectAndCompute(img1, None)
        keyP2, des2 = method.detectAndCompute(img2, None)

        mat = matcher.match(des1, des2)
        mat = sorted(mat, key=lambda x:x.distance)
        res = cv2.drawMatches(img1, keyP1, img2, keyP2, mat[0:20], None,
                              flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        cv2.imshow(name, res)

        matKnn = matcher.knnMatch(des1, des2, k=2)
        print(name, len(matKnn))
        if len(matKnn) >= minMatchCount:
            matKnnMask = [[0,0] for i in range(len(matKnn))]
            for i, (m, n) in enumerate(matKnn):
                if m.distance < 0.75 * n.distance:
                    matKnnMask[i] = [1, 0]


            drawParams = dict(matchColor=(0,255,0),
                              singlePointColor=(0,0,255),
                              matchesMask=matKnnMask[0:20],
                              flags=cv2.DrawMatchesFlags_DEFAULT)

            resKnn = cv2.drawMatches(img1,keyP1,img2,keyP2,matKnn[0:20],None,**drawParams)

# 마우스 이벤트
def mouse_callback(event, x, y, flags, param):
    global startX, startY, mouseDrawing
    imgROI = img1.copy()

    # 마우스 이벤트 시작 위치
    if event == cv2.EVENT_LBUTTONDOWN:
        mouseDrawing = True
        startX, startY = x, y
        cv2.circle(imgROI, (x,y), 2, (255, 255, 255), -1)
        cv2.imshow(viewName, imgROI)

    # 마우스 이동 위치
    elif event == cv2.EVENT_LBUTTONUP:
        if mouseDrawing:
            cv2.rectangle(imgROI, (startX,startY), (x,y), (255, 255, 255), 2)
            cv2.imshow(viewName, imgROI)

    # 마우스 이벤트 종료 위치
    elif event == cv2.EVENT_LBUTTONUP:
        mouseDrawing = False
        endX = x; endY = y
        # 마우스 움직임 보정
        if startX > endX:
            tempX = startX
            startX = endX; endX = tempX
        if startY > endY:
            tempY = startY
            startY = endY; endY = tempY

        cv2.rectangle(imgROI, (startX,startY), (endX,endY), (255,255,255), 2)
        cv2.imshow(viewName, imgROI)

        # 매칭 함수 호출
        roi = cv2.cvtColor(img1[startY:endY, startX:endX], cv2.COLOR_BGR2GRAY)
        BruteForce(roi,cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY))
        flann(roi, cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY))

# 영상 읽기
img1_src = cv2.imread("./images/img20.jpg", cv2.IMREAD_UNCHANGED)
img1 = cv2.resize(img1_src, (320,240))

# 마우스 이벤트 기반 특징 매칭
cv2.imshow(viewName, img1)
cv2.setMouseCallback(viewName, mouse_callback)

# 키보드 입력ㅇ르 기다린 후 모든 영상창 닫기
cv2.waitKey(0)
cv2.destroyAllWindows()
