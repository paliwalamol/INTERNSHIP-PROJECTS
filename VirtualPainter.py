import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

#######################
brushThickness = 8   
eraserThickness = 100
########################


folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
header = overlayList[0]

drawColor = (255, 0, 255)

cap = cv2.VideoCapture(1)

#this was the maximum resolution of my webcam
cap.set(3, 640)
cap.set(4, 480)

detector = htm.handDetector(detectionCon=0.85,maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros((480, 640, 3), np.uint8)


while True:

    # 1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # 2. Find Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # print(lmList)
        # tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)

        # 4. If Selection Mode - Two finger are up
        if fingers[1] and fingers[2] and fingers[3] and fingers[4]:
            # xp, yp = 0, 0
            print("Selection Mode")
            # # Checking for the click
            if y1 <= 80:
                if 128 < x1 < 256:
                    header = overlayList[0]
                    drawColor = (205, 255, 0)
                elif 256 < x1 < 384:
                    header = overlayList[1]
                    drawColor = (0, 255, 255)
                elif 384 < x1 < 512:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 512 < x1 < 640:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 15), (x2, y2 + 15), drawColor, cv2.FILLED)

        # 5. If Drawing Mode - Index finger is up
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
               xp, yp = x1, y1

            cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1


        # Clear Canvas when all fingers are up
        # if all (x >= 1 for x in fingers):
        #     imgCanvas = np.zeros((480, 640 , 3), np.uint8)

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)


    # Setting the header image
    img[0:80, 0:640] = header
    img = cv2.addWeighted(img,0.99,imgCanvas,0.5,0)
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)
    #cv2.imshow("Inv", imgInv)
    if cv2.waitKey(1) == ord('q'):
        break