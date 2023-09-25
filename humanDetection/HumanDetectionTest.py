# import the necessary packages
import numpy as np
import cv2



np.set_printoptions(suppress=True)
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# open video stream
# VideoCapture(0) == live camera view
cap = cv2.VideoCapture('AlotPPL.mov')

# Check if boxes are intersetcting 
def doIntersect(box1, box2):

    left0,bottom0,right0,top0 = box1
    # print(f'0:[x0:{x0a} y0:{y0a}],[x2:{x2a} y2:{y2a}] : {coefficienta}  ')
    left1,bottom1,right1,top1 = box2
    # print(f'1:[x1:{x1b} y1:{y1b}],[x1:{x1b} y1:{y1b}] : {coefficientb}  \n')
    
    # Check if rectangles are above eachother
    # Check if rectangles are left to eachother
    w = bottom0 < top1
    e = bottom1 < top0
    r = right0 < left1
    c = right1 < left0
    print(w,e,r,c)
    if bottom0 < top1 or bottom1 < top0 or right0 < left1 or right1 < left0:
        
        return False

    print('INTERSECT')
    return True

# If there are boxes intersecting chose one with highest coefficient
def NMS(coefficients):
    
    highestCoefficient = 0
    index = 0
    for i in range(len(coefficients)):
        if coefficients[i] > highestCoefficient:
            highestCoefficient = coefficients[i]
            index = i
        
    return index



while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # resizing for faster detection
    # find best resolution
    frame = cv2.resize(frame, (64*5, 128*5))
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )
    
    highestCoefficientIndex = 0

    if len(boxes) > 1:

        # print(len(boxes))
        if doIntersect(boxes[0], boxes[1]):
            
            highestCoefficientIndex = NMS(weights)
            boxes= np.array([boxes[highestCoefficientIndex]])
    
    #Debugg
    if len(boxes) > 1:
        print('Amount of boxes ', len(boxes))
        print(boxes, weights, '\n')
        


            

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    
    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
        cv2.putText(frame, str(x), (xA, yA-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)

