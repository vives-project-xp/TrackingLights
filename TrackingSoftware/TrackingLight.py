# import the necessary packages
import numpy as np
import cv2
import time

np.set_printoptions(suppress=True)

cv2.startWindowThread()

# open video stream
# VideoCapture(0) == live camera view
cap = cv2.VideoCapture('mov/hallway1.mov')

initialState = None  

while(True): 
    time.sleep(0.04)
    # Capture frame-by-frame
    ret, frame = cap.read()
    # find best resolution
    width = 640
    height = 360    
    # resizing for faster detection
    frame = cv2.resize(frame, (width, height))
    # Enhance brightness (increase all pixel values)
    bright_frame = cv2.convertScaleAbs(frame, alpha=2.2, beta=15)
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(bright_frame, cv2.COLOR_RGB2GRAY)

    # set gray threshold
    gray_frame = cv2.GaussianBlur(gray, (15, 1), 12)  

   # For the first iteration checking the condition

   # we will assign grayFrame to initalState if is none  

    if initialState is None:  

        initialState = gray_frame  
        continue  

    # Calculation of difference between static or initial and gray frame we created  

    differ_frame = cv2.absdiff(initialState, gray_frame)  

    # the change between static or initial background and current gray frame are highlighted 

    thresh_frame = cv2.threshold(differ_frame, 30, 255, cv2.THRESH_BINARY)[1]  

    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)  
    
    lineHeight = 215

    # check for white pixels on line (moving objects)
    # and draw rectangle at this place
    for i in range(0,width):
        if thresh_frame[lineHeight][i] == 255:
            cv2.rectangle(frame, (i-3,lineHeight-3), (i+3,lineHeight+3),(0,0,255) )

    # draw guidline which pixels are checked
    cv2.line(frame, (0,lineHeight), (width,lineHeight), (0,255,0),thickness=1)
    
    cv2.imshow('frame',frame)
    cv2.imshow('gray_frame',gray_frame)
    cv2.imshow('threshold', thresh_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)
