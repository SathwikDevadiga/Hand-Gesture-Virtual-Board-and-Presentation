import  cv2 
import mediapipe as mp
import time

class handDetector():
    def __init__(self,mode=False,MaxHands=2,dectectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.MaxHands = MaxHands
        self.dectectionCon = dectectionCon
        self.trackCon = trackCon
  
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.MaxHands)
        self.mpDraw = mp.solutions.drawing_utils

        self.tipIds = [4,8,12,16,20]

    def findHands(self,frame,draw=True):
         

        imgRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                         
                    self.mpDraw.draw_landmarks(frame,handLms,self.mpHands.HAND_CONNECTIONS)
                   
        return frame   
    def findPosition(self,frame,handNo=0,draw=True):  
        self.lmList = []      
        if self.results.multi_hand_landmarks:
            myHand =self.results.multi_hand_landmarks[handNo]

            for id , lm in enumerate(myHand.landmark):
                #print(id,lm)
                h,w,c = frame.shape
                cx , cy = int(lm.x*w), int(lm.y*h)
                
                self.lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(frame,(cx,cy),5,(255,0,0),cv2.FILLED)
        return self.lmList
    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

            # totalFingers = fingers.count(1)

        return fingers

def main():
    pTime = 0
    cTime = 0
    vid = cv2.VideoCapture(0) 

    dectector = handDetector()
    while(True): 
        
        # Capture the video frame 
        # by frame 
        success, frame = vid.read() 
        frame = dectector.findHands(frame)
        lmList = dectector.findPosition(frame)
        if len(lmList) !=0:
            print(lmList[0])

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(frame,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        # Display the resulting frame 
        cv2.imshow('frame', frame) 
        
        
        cv2.waitKey(1)
if __name__=="__main__":
     main()
