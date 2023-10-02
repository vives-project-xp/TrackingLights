import cv2
import time

GREEN = (0, 255, 0)
# initialize the HOG descriptor/person detector
#hog = cv2.HOGDescriptor()
#hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

body_detector = cv2.CascadeClassifier('det/haarcascade_fullbody.xml')
#body_detector = cv2.CascadeClassifier('det/haarcascade_frontalface_default.xml')
# Initialize variables for MeanShift tracking
track_window = None
roi_hist = None
term_crit = None

# initialize the camera object so that we
# can get frame from it
cap = cv2.VideoCapture('mov/front.mov')
#cap = cv2.VideoCapture('mov/back.mov')
#cap = cv2.VideoCapture('mov/ALL.mov')
#cap = cv2.VideoCapture('mov/zigzag.mov')

#cap = cv2.VideoCapture(0)

while True:
    time.sleep(0.10)    
    # reading the frame from camera
    _, frame = cap.read()
    
    # converting color image to gray scale image
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("test", gray_image)

    if track_window is not None:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
        
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)
        
        x, y, w, h = track_window
        cv2.rectangle(frame, (x, y), (x+w, y+h), GREEN, 2)

    else:
        # detecting bodies in the image
        body = body_detector.detectMultiScale(gray_image, scaleFactor=1.6, minNeighbors=1, minSize=(50, 100))
        # looping through the bodies detected in the image
        for (x, y, w, h) in body:
            cv2.rectangle(frame, (x, y), (x+w, y+h), GREEN, 2)

            # Initialize MeanShift tracking if a body is detected
            track_window = (x, y, w, h)
            roi = frame[y:y+h, x:x+w]
            hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv_roi, (0, 60, 32), (180, 255, 255))
            roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
            cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
            term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

    # show the frame on the screen
    cv2.imshow("frame", frame)

    # quit the program if you press 'q' on keyboard
    if cv2.waitKey(1) == ord("q"):
        break


cap.release()

# closing the windows that are opened
cv2.destroyAllWindows()
