import  cv2 
import mediapipe as mp
import time
import ht as htm


pTime = 0
cTime = 0
vid = cv2.VideoCapture(0) 

dectector = htm.handDetector()
while(True): 

    success, frame = vid.read() 
    frame = dectector.findHands(frame)
    lmList = dectector.findPosition(frame,draw=False)
    if len(lmList) !=0:
        print(lmList[0])

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(frame,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    # Display the resulting frame 
    cv2.imshow('frame', frame) 
    cv2.waitKey(1)