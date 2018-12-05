import numpy as np
import cv2
import datetime
from random import randint
import time

def GetDateTimeString():
    dt = str(datetime.datetime.now()).split(".")[0]
    clean = dt.replace(" ","_").replace(":","_")
    return clean

def GetBackground():
    bgImage = './bg/' + str(randint(1,4)) + '.jpg' 
    return cv2.imread(bgImage)

def GetImage(bg):
    ret, frame = cam.read()
    
    #Mask the green screen
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    image_mask=cv2.inRange(hsv,lowerBound,upperBound)
    bg_mask=cv2.bitwise_and(bg,bg,mask=image_mask)
    fg_mask=cv2.bitwise_and(frame,frame,mask=cv2.bitwise_not(image_mask))
    img = cv2.add(bg_mask,fg_mask)

    return img

def Calibrate():
    ret, frame = cam.read()
    hsv_screen = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    hueMax = hsv_screen[:,:,0].max()
    hueMin = hsv_screen[:,:,0].min()

    lowerBound = np.array([hueMin,0,0], np.uint8)
    upperBound = np.array([hueMax,255,255], np.uint8)

    text = "Calibrated!"
    textSize, base = cv2.getTextSize(text, fontFace, fontScale, thickness) 
    textWidth = (width - textSize[0])/2
    textHeight = (height + textSize[1])/2
    cv2.putText(frame,text,(textWidth,textHeight),fontFace,fontScale,(255,255,255),thickness)
    time.sleep(3)


#Setup window for full screen
cv2.namedWindow("Photobooth", cv2.WND_PROP_FULLSCREEN)          
cv2.setWindowProperty("Photobooth", cv2.WND_PROP_FULLSCREEN, 1)

#options for countdown timer
fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
thickness = 4
countdownSeconds = 5
displayPhotoSeconds = 5

#Setup WebCam
width = 640
height = 480

lowerBound = np.array([40,50,50])
upperBound = np.array([80,255,255])

cam = cv2.VideoCapture(0)
cam.set(3,width)
cam.set(4,height)

bg = GetBackground()
clicked = False
clickedTime = {}

while(True):
    img = GetImage(bg) #get masked image from webcam
    
    key = cv2.waitKey(1) #check for keypress
    if clicked == True : # if countdown timer started
        elapsed = datetime.datetime.now() - clickedTime
        secs = int(elapsed.total_seconds())
        if secs > countdownSeconds : # if five seconds are up, save the current image
            clicked = False
            cv2.imwrite('./out/' + GetDateTimeString() + '.jpg',img)
            cv2.imshow('Photobooth',img)
            time.sleep(displayPhotoSeconds) # show the photo for 5 seconds 
            bg = GetBackground() # get a new background
        else : # show the countdown timer
            text = str(5-secs) + "..."
            textSize, base = cv2.getTextSize(text, fontFace, fontScale, thickness) 
            textWidth = (width - textSize[0])/2
            textHeight = (height + textSize[1])/2
            cv2.putText(img,text,(textWidth,textHeight),fontFace,fontScale,(255,255,255),thickness)
    elif key == 32 : # on spacebar pressed, start the countdown timer
        clickedTime = datetime.datetime.now()
        clicked = True
    elif key == 9 : # on TAB - calibrate camera
        Calibrate()
    elif key == 27 : # on escape, close the program
        break
    
    cv2.imshow('Photobooth',img) #display masked image

cv2.destroyAllWindows()
cam.release()
