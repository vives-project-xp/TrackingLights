import numpy as np
import cv2
import time
import paho.mqtt.client as mqtt
import json

from Lights import Lights
from MqttObj import MqttController

#
lights = Lights()
mqtt_controller = MqttController()

# Initialize video capture
cap = cv2.VideoCapture('mov/output_video5.avi')

# Create a background subtractor
fgbg = cv2.createBackgroundSubtractorKNN()

# Initialize initialState
initialState = None

#siwtch case for different presets
switcher = {
    0:mqtt_controller.mqttTracking, 
    1:mqtt_controller.preset1,
    420:mqtt_controller.preset420
}
frames = 0
print("Program Started...")
while(True): 

    #Checking two heights for better detection
    baseLineHeight = 215
    middleHeight = 200
    headLineHeight = 181


    #Get active preset
    mqtt_controller_preset = mqtt_controller.getPreset()

    #Initialize list for detected pixels
    pixels = []

    # if default preset: start video and
    # and change lights if detected movement
    if(mqtt_controller_preset == 0):
        frames += 1

        # Capture frame-by-frame
        ret, frame = cap.read()
        # find best resolution
        width = 600 # *3
        height = 360 # *3
        time.sleep(0.01)

        #Resize frame
        frame = cv2.resize(frame, (width, height))
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        
        #Apply background subtraction
        # Cuse of learning rate, ppl who stand still for longer period of time will not be tracked
        fgmask = fgbg.apply(frame, None, 0.0008) 

        #Blur out the edges
        gray_frame = cv2.GaussianBlur(fgmask, (17,17), 0)             
            
        thresh_frame = cv2.threshold(gray_frame,20,255, cv2.THRESH_BINARY)[1]
                

        for i in range(0,width, 6):
            if thresh_frame[baseLineHeight][i] == 255 or thresh_frame[headLineHeight][i] == 255 or thresh_frame[200][i] == 255:
                cv2.rectangle(frame, (i-3,baseLineHeight-3), (i+3,baseLineHeight+3), [34,0,255] ,-1)
                #add detected pixels to list to be later grouped up
                pixels.append(i)

        #Send detected pixels list to grouping function
        pixels_group = lights.groupingPixels(pixels, mqtt_controller.getDetectionInput())



        #Send new json to mqtt controller
        switcher[mqtt_controller_preset](lights.getJson())

        

        #Draw green rectangles on image to see how detection works
        for group in pixels_group:
            if(len(group) < 1):
                break
            # Initialize values for image processing
            first_pixel = group[0]
            last_pixel = group[len(group)-1]

            cv2.rectangle(frame, (first_pixel, 205), (last_pixel, 225), (0,255,0), 2)



        # draw guideline which pixels are checked
        cv2.line(frame, (0,baseLineHeight), (width,baseLineHeight), (0,255,0),thickness=1)
        cv2.line(frame, (0,headLineHeight), (width,headLineHeight), (0,255,0),thickness=1)
        cv2.line(frame, (0,middleHeight), (width,middleHeight), (255,255,255),thickness=1)

        # Draw guideline on the threshold frame as well
        cv2.line(thresh_frame, (0,baseLineHeight), (width,baseLineHeight), (255,255,255),thickness=1)
        cv2.line(thresh_frame, (0,headLineHeight), (width,headLineHeight), (255,255,255),thickness=1)
        cv2.line(thresh_frame, (0,middleHeight), (width,middleHeight), (255,255,255),thickness=1)
        

        # cv2.imshow('frame', frame)
        # cv2.imshow('gray_frame', gray_frame)
        # cv2.imshow('threshold', thresh_frame)
        # cv2.imshow('backgroundDiff', fgmask)

        # # Move windows so they are properly placed
        # cv2.moveWindow('frame', 100,100)
        # cv2.moveWindow('threshold', 700,100)
        # cv2.moveWindow('backgroundDiff', 700,560)

    else:
        switcher[mqtt_controller_preset]()


    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
# Finally, close the window
#cv2.destroyAllWindows()
cv2.waitKey(1)
