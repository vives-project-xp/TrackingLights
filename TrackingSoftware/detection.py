import time
# install opencv "pip install opencv-python"
import cv2

GREEN = (0, 255, 0)

body_detector = cv2.CascadeClassifier('det/haarcascade_fullbody.xml')

# initialize the camera object so that we
# can get frame from it
cap = cv2.VideoCapture('mov/front.mov')
#cap = cv2.VideoCapture('mov/back.mov')
#cap = cv2.VideoCapture('mov/ALL.mov')
#cap = cv2.VideoCapture('mov/zigzag.mov')

#cap = cv2.VideoCapture(0)

# looping through frame, incoming from
# camera/video
while True:
	time.sleep(0.05)
	# reading the frame from camera
	_, frame = cap.read()
	
    	# converting color image to gray scale image
	gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY )
	cv2.imshow("test", gray_image)

	# detecting face in the image
	body = body_detector.detectMultiScale(gray_image, scaleFactor=1.6, minNeighbors=1, minSize=(50, 100))

	# looping through the faces detect in the image
	# getting coordinates x, y , width and height
	for (x, y, w, h) in body:

		# draw the rectangle on the face
		cv2.rectangle(frame, (x, y), (x+w, y+h), GREEN, 2)

	# show the frame on the screen
	cv2.imshow("frame", frame)


	# quit the program if you press 'q' on keyboard
	if cv2.waitKey(1) == ord("q"):
		break

# closing the camera
cap.release()

# closing the windows that are opened
cv2.destroyAllWindows()
