# import the necessary packages
import numpy as np
import cv2
import time
import paho.mqtt.client as mqtt
import json


# Set up MQTT client
mqtt_client = mqtt.Client()
mqtt_client.connect("mqtt.devbit.be", 1883, 60)

data = {'leds': [0]}

np.set_printoptions(suppress=True)

cv2.startWindowThread()

# open video stream
# VideoCapture(0) == live camera view
cap = cv2.VideoCapture('mov/hallway1.mov')
fgbg = cv2.createBackgroundSubtractorMOG2()
 

initialState = None  

while(True): 
    time.sleep(0.0)
    # Capture frame-by-frame
    ret, frame = cap.read()
    # find best resolution
    width = 600
    height = 360    
    # resizing for faster detection
    frame = cv2.resize(frame, (width, height))
    
    # apply background subtraction
    fgmask = fgbg.apply(frame, None, 0) 
    # Enhance brightness (increase all pixel values)
    # bright_frame = cv2.convertScaleAbs(frame, alpha=1, beta=20)

    # Blur out the edges
    gray_frame = cv2.GaussianBlur(fgmask, (21,21), 0)  

   # For the first iteration checking the condition

   # we will assign grayFrame to initalState if is none  


    if initialState is None:  

        initialState = gray_frame  
        continue  

    # Calculation of difference between static or initial and gray frame we created  

    # differ_frame = cv2.absdiff(initialState, gray_frame)  

    # the change between static or initial background and current gray frame are highlighted 

    thresh_frame = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY)[1]  

    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)  
    
    lineHeight = 215
    # Create a copy of the 'leds' list
    leds_copy = []

    # check for white pixels on line (moving objects)
    # and draw rectangle at this place
    for i in range(0,width, 3):
        if thresh_frame[lineHeight][i] == 255 or thresh_frame[181][i]==255:
            if i % 6 == 0:
                leds_copy.append(1)
            cv2.rectangle(frame, (i-3,lineHeight-3), (i+3,lineHeight+3),(0,0,255) )
        else:
            if i % 6 == 0:
                leds_copy.append(0)

    # Now assign the modified 'leds_copy' back to 'leds'
    # Inside the loop, after motion detection and before publishing to MQTT

    data['leds'] = leds_copy
    json_data = json.dumps(data)  # Convert the dictionary to a JSON string
    mqtt_client.publish("topic/TrackingLights/cameraDetectionArray", json_data)
    print(json_data)

    leds_copy*=0

    # draw guidline which pixels are checked
    cv2.line(frame, (0,lineHeight), (width,lineHeight), (0,255,0),thickness=1)
    cv2.line(frame, (0,181), (width,181), (0,255,0),thickness=1)
    
    cv2.imshow('frame',frame)
    cv2.imshow('threshold', thresh_frame)
    cv2.imshow('backgroundDiff', fgmask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
# Disconnect from MQTT broker
mqtt_client.disconnect()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)
