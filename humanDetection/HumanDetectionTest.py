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
cap = cv2.VideoCapture('2DTest.mov')

initialState = None  

# Check if boxes are intersetcting 
def doIntersect(box1, box2):

    left0,bottom0,right0,top0 = box1
    # print(f'0:[x0:{x0a} y0:{y0a}],[x2:{x2a} y2:{y2a}] : {coefficienta}  ')
    left1,bottom1,right1,top1 = box2
    # print(f'1:[x1:{x1b} y1:{y1b}],[x1:{x1b} y1:{y1b}] : {coefficientb}  \n')
    
    # Check if rectangles are above eachother
    # Check if rectangles are left to eachother
    # If everything is fales then they are intersecting
    w = bottom0 < top1
    e = bottom1 < top0
    r = right0 < left1
    c = right1 < left0
    # print(w,e,r,c)
    if bottom0 < top1 or bottom1 < top0 or right0 < left1 or right1 < left0:
        
        return False

    # print('INTERSECT')
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

# Malisiewicz et al.
def non_max_suppression_fast(boxes, overlapThresh):
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []
    # if the bounding boxes integers, convert them to floats --
    # this is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")
    # initialize the list of picked indexes    
    pick = []
    # grab the coordinates of the bounding boxes
    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,2]
    y2 = boxes[:,3]
    # compute the area of the bounding boxes and sort the bounding
    # boxes by the bottom-right y-coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)
    # keep looping while some indexes still remain in the indexes
    # list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        # compute the width and height of the bounding box

        # need to fix maximum of next arrays
        w = np.array(xx2 - xx1 + 1).astype("float")
        h = np.array(yy2 - yy1 + 1).astype("float")

        print(xx2, xx1)

        print('-----')
        print(w)
        print(h)
        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]
        # print(f'{w} * {h} / {area[idxs[:last]]}')
        print(f'overlap: {overlap}')
        idxs = np.delete(idxs, np.concatenate(([last],
            np.where(overlap > overlapThresh)[0])))
    # return only the bounding boxes that were picked using the
    # integer data type

 
    return boxes[pick].astype("int")



while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # resizing for faster detection
    # find best resolution
    frame = cv2.resize(frame, (64*7, 128*5))
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    #Testing with GrayTreshold
    gray_frame = cv2.GaussianBlur(gray, (21, 21), 0)  


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
    
        # detect people in the image
        # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )
    
    highestCoefficientIndex = 0

    # if len(boxes) > 1:

        # print(len(boxes))
        # if doIntersect(boxes[0], boxes[1]):
            
    boxes = non_max_suppression_fast(boxes, 0.4)
            
            # boxes= np.array([boxes[highestCoefficientIndex]])
            
    
    #Debugg
    # if len(boxes) > 1:
        # print('Amount of boxes ', len(boxes))
    #     print(boxes, weights, '\n')
        


            

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    
    x = 0
    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
        cv2.putText(frame, str(x), (xA, yA-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        x +=1
    # Display the resulting frame
    
    cv2.imshow('frame',frame)
    cv2.imshow('treshold', thresh_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)

