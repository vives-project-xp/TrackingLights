import numpy as np
import cv2
import time
import paho.mqtt.client as mqtt
import json

white = [255, 255, 255]
detected_color = [244, 0, 32] # vives_red as base

# Define MQTT broker details
broker_address = "mqtt.devbit.be"
port = 1883


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
    'bri': 100,
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

group = {
    'on': True,
    'bri': 100,
    "seg":{"i":[0,0, detected_color, 100,100, detected_color]}}

color = {'color': [255, 255, 255]}
preset = {'pr': 1}

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to topics on successful connection
    client.subscribe([(brightness_topic, 0), (color_topic, 0), (on_off_topic, 0), (preset_topic, 0)])

# Callback when a message is received from the broker
def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}: {message.payload.decode()}")
    
    # # Create JSON string based on the received message
    # if message.topic == on_off_topic:
    #     data['on'] = message.payload.decode()
    # if message.topic == brightness_topic:     
    #     data['on'] = message.payload.decode()
    # if message.topic == color_topic():
    #     color = message.payload.decode()
    # if message.topic == preset_topic:
    #     preset = message.payload.decode()
    print(f"JSON representation: {data} {color} {preset}")

# Set up MQTT client
mqtt_client = mqtt.Client()
# mqtt_client.on_connect = on_connect
# mqtt_client.on_message = on_message
mqtt_client.connect(broker_address, port, 60)

# Start MQTT loop (non-blocking)
mqtt_client.loop_start()



# Initialize video capture
cap = cv2.VideoCapture('mov/hallway1.mov')

# Create a background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

# Initialize initialState
initialState = None

while(True): 
    
    time.sleep(0.03)
    # Capture frame-by-frame
    ret, frame = cap.read()

    # find best resolution
    width = 600 # *3
    height = 360 # *3
    # resizing for faster detection
    frame = cv2.resize(frame, (width, height))
    # apply background subtraction
    fgmask = fgbg.apply(frame, None, 0) 

    # Blur out the edges
    gray_frame = cv2.GaussianBlur(fgmask, (21,21), 0)  

   # we will assign grayFrame to initalState if is none  
    if initialState is None:  
        initialState = gray_frame  
        continue  

    thresh_frame = cv2.threshold(gray_frame, 100, 255, cv2.THRESH_BINARY)[1]  
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)  
        
    # checking two heights for better detection
    baseLineHeight = 215
    headLineHeight = 181

    # Create a copy of the 'leds' list
    i_color = white
    i_group = []
    pixels = []

    # check for white pixels on line (moving objects)
    # and draw rectangle at this place
    for i in range(0,width, 6):
        if thresh_frame[baseLineHeight][i] == 255 or thresh_frame[headLineHeight][i] == 255:
            cv2.rectangle(frame, (i-3,baseLineHeight-3), (i+3,baseLineHeight+3), list(reversed(detected_color)) ,-1)

            ## pixels that detect motion add to list
            ## then group pixels that are not further from eachother than x
            ## and draw another rectangle at begining and ending of pixels_groups (array of arrays)
            pixels.append(i)
            

    ## For better performance you can put it in first loop
    # put pixels in groups
    pixels_group = [[]]
    group_index = 0
    for i in range(1, len(pixels)-1):
        pixels_distance = pixels[i] - pixels[i-1]
        #print(pixels_distance)

        # if pixels distance is not greater than 20 pixels group them up
        if(pixels_distance < 50):
            pixels_group[group_index].append(pixels[i-1])
            pixels_group[group_index].append(pixels[i])

        else:
            
            group_index += 1
            pixels_group.append([])

    newJson = { 
        "on": True,
        "bri": 100,
        "seg":{"i":[0,100, 'FFFFFF']}}

    for group in pixels_group:

        if(len(group) < 1):
            break
        
        # Initialize values for image processing
        first_pixel = group[0]
        last_pixel = group[len(group)-1]
        cv2.rectangle(frame, (first_pixel, 205), (last_pixel, 225), (0,255,0), 2)

        # Divide by 6 > each segment of leds = 6leds
        first_pixel = int(group[0]/6)
        last_pixel = int(group[len(group)-1]/6)

        distance_betweeen_pixels = last_pixel - first_pixel

        # Add minimum distance (for leds)
        minimum_distance = 20
        two_segments = 12

        # if(distance_betweeen_pixels < minimum_distance):
            
            # add three segments to lenght if its too short
            # if(last_pixel > 100): last_pixel = 100
            # if(first_pixel < 0 ): first_pixel = 0       

        newJson["seg"]["i"].append(first_pixel-3)
        newJson["seg"]["i"].append(last_pixel+3)
        newJson["seg"]["i"].append("C00000")

        newJson["seg"]["i"].append(first_pixel-1)
        newJson["seg"]["i"].append(last_pixel+1)
        newJson["seg"]["i"].append("F50000")
        
        newJson["seg"]["i"].append(first_pixel)
        newJson["seg"]["i"].append(last_pixel)
        newJson["seg"]["i"].append("FF0000")

       
    # json_data = json.dumps(data) 
    newJson = json.dumps(newJson)

    # print(newJson)
    mqtt_client.publish("TrackingLights/leddriver/api", newJson)



    # draw guideline which pixels are checked
    cv2.line(frame, (0,baseLineHeight), (width,baseLineHeight), (0,255,0),thickness=1)
    cv2.line(frame, (0,headLineHeight), (width,headLineHeight), (0,255,0),thickness=1)

    # Draw guideline on the threshold frame as well
    cv2.line(thresh_frame, (0,baseLineHeight), (width,baseLineHeight), (255,255,255),thickness=1)
    cv2.line(thresh_frame, (0,headLineHeight), (width,headLineHeight), (255,255,255),thickness=1)

    cv2.imshow('frame', frame)
    cv2.imshow('threshold', thresh_frame)
    cv2.imshow('backgroundDiff', fgmask)

    # Move windows so they are properly placed
    cv2.moveWindow('frame', 100,100)
    cv2.moveWindow('threshold', 700,100)
    cv2.moveWindow('backgroundDiff', 700,560)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything is done, release the capture
cap.release()
# Disconnect from MQTT broker
mqtt_client.disconnect()
# Finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)


