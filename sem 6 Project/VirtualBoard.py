import  cv2 
import mediapipe as mp
import time
import numpy as np
import os
import ht as htm


brushThickness =15
eraserThickness = 50
xp,yp = 0,0
imgCanva = np.zeros((720,1280,3),np.uint8)


folderPath = "header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
header = overlayList[0]
drawColor = (255, 0, 255)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = htm.handDetector(MaxHands=1)

tipIds = [4,8,12,16,20]

while True:
    success, frame = cap.read() 

    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)

    if len(lmList) != 0:

        # print(lmList)

        # tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()
        print(fingers)

        if fingers[1] and fingers[2]:
            # xp, yp = 0, 0
            
            print("Selection Mode")
            if y1 < 125:
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
            cv2.rectangle(frame,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)

        if fingers[1] and fingers[2] == False:
            cv2.circle(frame, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            
            if drawColor==(0,0,0):
                cv2.line(frame, (xp, yp), (x1, y1), drawColor, eraserThickness) 
                cv2.line(imgCanva, (xp, yp), (x1, y1), drawColor, brushThickness)
            else:
                cv2.line(frame, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanva, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp,yp=x1,y1

    frame[0:125,0:1280] = header
    frame = cv2.addWeighted(frame,0.5,imgCanva,0.5,0) 
    cv2.imshow("Image", frame) 
    cv2.imshow("CANVAS", imgCanva) 
    cv2.waitKey(1)
