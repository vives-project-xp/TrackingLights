import numpy as np
import cv2
import time
import paho.mqtt.client as mqtt
import json

# Set up MQTT client
mqtt_client = mqtt.Client()
mqtt_client.connect("mqtt.devbit.be", 1883, 60)

# Define MQTT topics for brightness and color
brightness_topic = "TrackingLights/brightness"
color_topic = "TrackingLights/color"
on_off_topic = "TrackingLights/on_off"
preset_topic = "TrackingLights/preset"

# Define initial LED data dictionary
#ledsData = {'leds': [0]}

# Define initial data dictionary for brightness and color values 
# We have 100 segments 
data = {
    'on': True,
    'bri': 255,
    'seg': {'i':[[255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255],
                 [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255],
                 [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255],
                 [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255],
                 [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255],
                 [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255],
                 [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255],
                 [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255],
                 [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255],
                 [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255], [255,255,255],]}
}

color = {'color' : [255, 255, 255]}
preset = {'pr': 1}

# Define callback functions for MQTT
def on_brightness_message(client, userdata, message):
    data['bri'] = int(message.payload.decode())
    print(*message.topic,str(message.payload.decode()))

def on_color_message(client, userdata, message):
    color['color'] = json.loads(message.payload.decode())
    print(*message.topic,str(message.payload.decode()))


def on_on_off_message(client, userdata, message):
    data['on'] = json.loads(message.payload.decode())
    print(*message.topic,str(message.payload.decode()))


# Define callback functions for MQTT
def on_preset_message(client, userdata, message):
    preset['pr'] = int(message.payload.decode())
    print(*message.topic,str(message.payload.decode()))


# Subscribe to MQTT topics
mqtt_client.subscribe(brightness_topic)
mqtt_client.subscribe(color_topic)
mqtt_client.subscribe(on_off_topic)
mqtt_client.subscribe(preset_topic)

# Set MQTT callbacks
mqtt_client.message_callback_add(brightness_topic, on_brightness_message)
mqtt_client.message_callback_add(color_topic, on_color_message)
mqtt_client.message_callback_add(on_off_topic, on_on_off_message)
mqtt_client.message_callback_add(preset_topic, on_preset_message)


# Initialize video capture
cap = cv2.VideoCapture('mov/hallway2.mov')

# Create a background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

# Initialize initialState
initialState = None

white = [255, 255, 255]
detected_color = [244, 0, 32] # vives_red as base

while(True): 

    time.sleep(0.05)
    # Capture frame-by-frame
    ret, frame = cap.read()

    # find best resolution
    width = 600 # *3
    height = 360 # *3
    # resizing for faster detection
    frame = cv2.resize(frame, (width, height))
    # apply background subtraction
    fgmask = fgbg.apply(frame, None, 0) 
    # Enhance brightness (increase all pixel values)
    bright_frame = cv2.convertScaleAbs(fgmask, alpha=1, beta=20)
    # Blur out the edges
    gray_frame = cv2.GaussianBlur(bright_frame, (21,21), 0)  

   # we will assign grayFrame to initalState if is none  
    if initialState is None:  
        initialState = gray_frame  
        continue  

    thresh_frame = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY)[1]  
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)  
        
    #baseLineHeight = 645
    baseLineHeight = 215
    headLineHeight = 181

    # Create a copy of the 'leds' list
    leds_copy = []
    i_color = white

    # check for white pixels on line (moving objects)
    # and draw rectangle at this place
    for i in range(0,width, 6):
        if thresh_frame[baseLineHeight][i] == 255 or thresh_frame[headLineHeight][i] == 255:
            leds_copy.append(detected_color)
            cv2.rectangle(frame, (i-3,baseLineHeight-3), (i+3,baseLineHeight+3), list(reversed(detected_color)) ,-1)
        else:
            leds_copy.append(white)
        
    i_color = leds_copy
    data['seg']['i'] = i_color

    # Now assign the modified 'leds_copy' back to 'leds'
    #ledsData['leds'] = leds_copy
    #ledsArray = json.dumps(ledsData) 
    #mqtt_client.publish("TrackingLights/cameraDetectionArray", ledsArray)

    json_data = json.dumps(data)  
    leds_copy*=0
    
    #if(count % 2 == 0):
    mqtt_client.publish("TrackingLights/leddriver/api", json_data)
    #count = count + 1

    # draw guideline which pixels are checked
    cv2.line(frame, (0,baseLineHeight), (width,baseLineHeight), (0,255,0),thickness=1)
    cv2.line(frame, (0,headLineHeight), (width,headLineHeight), (0,255,0),thickness=1)

    # Draw guideline on the threshold frame as well
    cv2.line(thresh_frame, (0,baseLineHeight), (width,baseLineHeight), (255,255,255),thickness=1)
    cv2.line(thresh_frame, (0,headLineHeight), (width,headLineHeight), (255,255,255),thickness=1)

    cv2.imshow('frame', frame)
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

