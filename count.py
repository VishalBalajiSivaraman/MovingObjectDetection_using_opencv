import imutils
import cv2
import time# delay introduction and so on
cam=cv2.VideoCapture(0)#0-inbuilt cam,1-2nd camera,2-3rd camera ,so on
time.sleep(1)#in seconds
count=0
firstFrame=None# capturing bg
area = 500# capturing the area required
while True:
    _,img=cam.read()
    text= "Normal"
    img=imutils.resize(img,width=500)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gauss=cv2.GaussianBlur(gray, (21,21),0)
    if firstFrame is None:
        firstFrame = gauss
        continue
    imgDiff=cv2.absdiff(firstFrame,gray)#comparing first frame with grey scale image
    thresh=cv2.threshold(imgDiff,25,255,cv2.THRESH_BINARY)[1]
    thresh=cv2.dilate(thresh,None,iterations=2)# outlines are dilate  to make them go away we use erode fn and to remove distortions in image we use dilate fn 
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts=imutils.grab_contours(cnts)#contours are used to connect neighborhood pixels
    for c in cnts:
         if cv2.contourArea(c)<area:
             continue
         (x,y,w,h)=cv2.boundingRect(c)
         count+=1
         cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0),2)
         text="Moving Object Detected"
         TEXT= "Count :"+str(count)
         print(text)
         print(count)
         cv2.putText(img, text, (10,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
         cv2.putText(img, TEXT, (10,70),cv2.FONT_HERSHEY_SIMPLEX, 1,(5,250,5), 1)
         cv2.imshow("camerafeed",img)
         key = cv2.waitKey(1) & 0xFF # cv2.waitkey represents 32 bit value whereas 0xff represent 8 bit value
         if key == ord("q"):# indicates the user that if he presses q the fn will get terminated
             break
cam.release()#release your camera and avoid errors
cv2.destroyAllWindows()
