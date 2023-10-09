# import the necessary packages
import numpy as np
import cv2
import time
import paho.mqtt.client as mqtt
import json

# Set up MQTT client
mqtt_client = mqtt.Client()
mqtt_client.connect("mqtt.devbit.be", 1883, 60)

# Define initial LED data dictionary
ledsData = {'leds': [0]}

# Define initial data dictionary for brightness and color values
data = {'on': True , 'bri': 255, 'seg': {'i':[[255,255,255], [255,255,255], [255,255,255]]}}

np.set_printoptions(suppress=True)

cv2.startWindowThread()

# open video stream
# VideoCapture(0) == live camera view
cap = cv2.VideoCapture('mov/hallway1.mov')

fgbg = cv2.createBackgroundSubtractorMOG2()

initialState = None  

# Define MQTT topics for brightness and color
brightness_topic = "TrackingLights/brightness"
color_topic = "TrackingLights/color"
count = 0
# Define callback functions for MQTT
def on_brightness_message(client, userdata, message):
    data['bri'] = int(message.payload.decode())

def on_color_message(client, userdata, message):
    data['col'] = json.loads(message.payload.decode())

# Subscribe to MQTT topics
mqtt_client.subscribe(brightness_topic)
mqtt_client.subscribe(color_topic)

# Set MQTT callbacks
mqtt_client.message_callback_add(brightness_topic, on_brightness_message)
mqtt_client.message_callback_add(color_topic, on_color_message)

while(True): 
    time.sleep(0.00)
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


    # the change between static or initial background and current gray frame are highlighted 

    thresh_frame = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY)[1]  


    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)  
    
    baseLineHeight = 215
    headLineHeight = 181
    # Create a copy of the 'leds' list
    leds_copy = []
    i_color = [255, 255, 255]

    # check for white pixels on line (moving objects)
    # and draw rectangle at this place
    for i in range(0,width, 6):
        if thresh_frame[baseLineHeight][i] == 255 or thresh_frame[headLineHeight][i] == 255:
            leds_copy.append([224, 0, 32])
            cv2.rectangle(frame, (i-3,baseLineHeight-3), (i+3,baseLineHeight+3),(0,0,255) )
        else:
            leds_copy.append([255,255,255])
        
    i_color = leds_copy
    data['seg']['i'] = i_color
    json_data = json.dumps(data)  
    
    #if(count % 2 == 0):
    mqtt_client.publish("TrackingLights/leddriver/api", json_data)
    #count = count + 1

    # Now assign the modified 'leds_copy' back to 'leds'
    ledsData['leds'] = leds_copy
    ledsArray = json.dumps(ledsData)  # Convert the dictionary to a JSON string
    #mqtt_client.publish("TrackingLights/cameraDetectionArray", ledsArray)

    leds_copy*=0

    # draw guideline which pixels are checked
    cv2.line(frame, (0,baseLineHeight), (width,baseLineHeight), (0,255,0),thickness=1)
    cv2.line(frame, (0,headLineHeight), (width,headLineHeight), (0,255,0),thickness=1)

    # Draw guideline on the threshold frame as well
    cv2.line(thresh_frame, (0,baseLineHeight), (width,baseLineHeight), (255,255,255),thickness=1)
    cv2.line(thresh_frame, (0,headLineHeight), (width,headLineHeight), (255,255,255),thickness=1)

    cv2.imshow('frame',frame)
    cv2.imshow('threshold', thresh_frame)
    cv2.imshow('backgroundDiff', fgmask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
# Disconnect from MQTT broker
mqtt_client.disconnect()
# Finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)

