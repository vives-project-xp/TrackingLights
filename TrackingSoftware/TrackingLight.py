import cv2
import numpy as np

# Function to detect motion and generate black and white mask


def detect_motion(frame1, frame2, threshold=30):
    delta_frame = cv2.absdiff(frame1, frame2)
    gray_frame = cv2.cvtColor(delta_frame, cv2.COLOR_BGR2GRAY)
    _, threshold_frame = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
    return threshold_frame


# Load video file
cap = cv2.VideoCapture('mov/hallway1.mov')

# Read the first frame
ret, first_frame = cap.read()

# Process video frames
while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convert frames to grayscale and apply GaussianBlur for better results
    gray_frame1 = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
    gray_frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame1 = cv2.GaussianBlur(gray_frame1, (21, 21), 0)
    gray_frame2 = cv2.GaussianBlur(gray_frame2, (21, 21), 0)

    # Get the motion detection mask
    motion_mask = detect_motion(gray_frame1, gray_frame2)

    # Find contours of moving objects
    contours, _ = cv2.findContours(motion_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create black and white image with moving areas
    moving_areas = np.zeros_like(frame)
    cv2.drawContours(moving_areas, contours, -1, (255, 255, 255), thickness=cv2.FILLED)

    # Display the moving areas
    cv2.imshow('Moving Areas', moving_areas)

    # Show the original video with moving areas highlighted
    cv2.imshow('Original Video with Moving Areas', cv2.add(frame, moving_areas))

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Update the first frame
    first_frame = frame.copy()

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
