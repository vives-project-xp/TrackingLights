import numpy as np
import cv2
import time
import paho.mqtt.client as mqtt
import json


#
# lights = Lights()
# mqtt_controller = MqttController()

# Initialize video capture
cap = cv2.VideoCapture('mov/hallway2.mov')

# Create a background subtractor
fgbgMOG = cv2.createBackgroundSubtractorMOG2()
fgbgKNN = cv2.createBackgroundSubtractorKNN()

# Initialize initialState
initialState = None

#siwtch case for different presets
# switcher = {
#     0:mqtt_controller.mqttTracking, 
#     1:mqtt_controller.preset1,
#     2:mqtt_controller.preset2,
#     3:mqtt_controller.preset3,
#     420:mqtt_controller.preset420
# }

while(True): 

    #Checking two heights for better detection
    baseLineHeight = 215
    headLineHeight = 181

    #Get active preset
    # mqtt_controller_preset = mqtt_controller.getPreset()

    #Initialize list for detected pixels
    pixels = []

    # if default preset: start video and
    # and change lights if detected movement
    # if(mqtt_controller_preset == 0):

    # Capture frame-by-frame
    ret, frame = cap.read()
    time.sleep(0.01)
    # find best resolution
    width = 600 # *3
    height = 360 # *3

    #Resize frame
    frame = cv2.resize(frame, (width, height))
    frame = cv2.rotate(frame, cv2.ROTATE_180)

    #Apply background subtraction
    # Cuse of learning rate, ppl who stand still for longer period of time will not be tracked
    fgmaskKNN = fgbgKNN.apply(frame, None, 0.0008) 
    fgmaskMOG = fgbgMOG.apply(frame, None, 0.0008) 

    #Blur out the edges
    gray_frameKNN = cv2.GaussianBlur(fgmaskKNN, (21,21), 0)  
    gray_frameMOG = cv2.GaussianBlur(fgmaskMOG, (21,21), 0)  

    # we will assign grayFrame to initalState if is none  
    if initialState is None:  
        initialState = gray_frameKNN
        continue  

    thresh_frameKNN = cv2.threshold(gray_frameKNN, 100, 255, cv2.THRESH_BINARY)[1]  
    thresh_frameMOG = cv2.threshold(gray_frameMOG, 100, 255, cv2.THRESH_BINARY)[1]  


    thresh_frameKNN = cv2.dilate(thresh_frameKNN, None, iterations = 2) 
    thresh_frameMOG = cv2.dilate(thresh_frameMOG, None, iterations = 2)  

    counturs = cv2.findContours(thresh_frameKNN,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    for i in counturs:
        print(i)
        

    # for i in range(0,width, 6):
    #     if thresh_frame[baseLineHeight][i] == 255 or thresh_frame[headLineHeight][i] == 255 or thresh_frame[200][i] == 255:
    #         cv2.rectangle(frame, (i-3,baseLineHeight-3), (i+3,baseLineHeight+3), [34,0,255] ,-1)
    #         #add detected pixels to list to be later grouped up
    #         pixels.append(i)

    # #Send detected pixels list to grouping function
    # pixels_group = lights.groupingPixels(pixels, mqtt_controller.getDetectionInput())



    # #Send new json to mqtt controller
    # switcher[mqtt_controller_preset](lights.getJson())

    

    #Draw green rectangles on image to see how detection works
    # for group in pixels_group:
    #     if(len(group) < 1):
    #         break
    #     # Initialize values for image processing
    #     first_pixel = group[0]
    #     last_pixel = group[len(group)-1]

    #     cv2.rectangle(frame, (first_pixel, 205), (last_pixel, 225), (0,255,0), 2)



    # draw guideline which pixels are checked
    # cv2.line(frame, (0,baseLineHeight), (width,baseLineHeight), (0,255,0),thickness=1)
    # cv2.line(frame, (0,headLineHeight), (width,headLineHeight), (0,255,0),thickness=1)

    # # Draw guideline on the threshold frame as well
    # cv2.line(gray_frameKNN, (0,baseLineHeight), (width,baseLineHeight), (255,255,255),thickness=1)
    # cv2.line(gray_frameKNN, (0,headLineHeight), (width,headLineHeight), (255,255,255),thickness=1)
    # cv2.line(gray_frameKNN, (0,200), (width,200), (255,255,255),thickness=1)
    

    cv2.imshow('frame', frame)
    cv2.imshow('thresholdKNN', thresh_frameKNN)
    cv2.imshow('thresholdMOG', thresh_frameMOG)
    cv2.imshow('backgroundDiffKNN', fgmaskKNN)
    cv2.imshow('backgroundDiffMOG', fgmaskMOG)

    # Move windows so they are properly placed
    cv2.moveWindow('frame', 100,100)
    cv2.moveWindow('thresholdKNN', 700,100)
    cv2.moveWindow('backgroundDiffKNN', 700,560)

    # else:
    #     switcher[mqtt_controller_preset]()


    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
# Finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)



