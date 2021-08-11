import cv2
import mediapipe as mp
import pyautogui


cap = cv2.VideoCapture(1)

#this was the maximum resolution of my webcam
cap.set(3, 640)
cap.set(4, 480)
 
mp_face_mesh =  mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

a=0
b=0
c=0
d=0

while True:

    # 1. Import image
    success, img = cap.read()

    img = cv2.flip(img, 1)

    rgb_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    

    
    result = face_mesh.process(rgb_img)
    

    if result.multi_face_landmarks:
        for facial_landmarks in result.multi_face_landmarks:
            pt1 = facial_landmarks.landmark[1]
            x = int(pt1.x * 640)
            y = int(pt1.y * 480)
            # print(x,y)
            cv2.circle(img,(x,y),5,(100,100,0),-1)
            if(y>260):
                print("down arrow key")
                if b==1:
                    pyautogui.keyUp('up')
                    b=0
                if c==1:
                    pyautogui.keyUp('left')
                    c=0
                if d==1:
                    pyautogui.keyUp('right')
                    d=0
                  
                pyautogui.keyDown('down')
                a=1
            elif(y<200):
                if a==1:
                    pyautogui.keyUp('down')
                    a=0
                if d==1:
                    pyautogui.keyUp('right')
                    d=0
                if c==1:
                    pyautogui.keyUp('left')
                    c=0
                print("up arrow key")
                pyautogui.keyDown('up')
                b=1
            elif(x<282):
                if a==1:
                    pyautogui.keyUp('down')
                    a=0
                if d==1:
                    pyautogui.keyUp('right')
                    d=0
                if b==1:
                    pyautogui.keyUp('up')
                    b=0
                print("left arrow key")
                pyautogui.keyDown('left')
                c=1
            elif(x>360):
                if a==1:
                    pyautogui.keyUp('down')
                    a=0
                if b==1:
                    pyautogui.keyUp('up')
                    b=0
                if c==1:
                    pyautogui.keyUp('left')
                    c=0
                print("right arrow key")
                pyautogui.keyDown('right')
                d=1
            else:
                if a==1:
                    pyautogui.keyUp('down')
                    a=0
                if b==1:
                    pyautogui.keyUp('up')
                    b=0
                if d==1:
                    pyautogui.keyUp('right')
                    pyautogui.keyDown('left')
                    d=0
                if c==1:
                    pyautogui.keyUp('left')
                    pyautogui.keyDown('right')
                    c=0
                
                print("no key")


    cv2.line(img, (280,0), (280, 480), (255,255,255), 2)
    cv2.line(img, (360,0), (360, 480), (255,255,255), 2)
    cv2.line(img, (0,200), (640, 200), (255,255,255), 2)
    cv2.line(img, (0,260), (640, 260), (255,255,255), 2)
    cv2.imshow("Image", img)
    #cv2.imshow("Image2", rgb_img)








    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
