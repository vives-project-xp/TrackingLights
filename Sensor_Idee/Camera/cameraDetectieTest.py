# import the opencv library
import cv2
import numpy as np

from object_detection import ObjectDetection 

od = ObjectDetection()

# define a video capture object
vid = cv2.VideoCapture("los_angeles.mp4")

center_points_cur_frame = []

while(True):
	
	# Capture the video frame
	# by frame
	ret, frame = vid.read()

	# Display the resulting frame
	cv2.imshow('frame', frame)
	
    # Detect objects on frame
	(class_ids, scores, boxes) = od.detect(frame)
	for box in boxes:
		(x, y, w, h) = box
		cx = int((x + x + w) / 2)
		cy = int((y + y + h) / 2)
		center_points_cur_frame.append((cx,cy))
        
	# the 'q' button is set as the
	# quitting button you may use any
	# desired button of your choice
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()




