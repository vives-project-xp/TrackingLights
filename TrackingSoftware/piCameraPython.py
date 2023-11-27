import cv2

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for the video file
fps = 30.0  # Frames per second
output_file = 'output_video.avi'  # Output video file name
video_capture = cv2.VideoCapture(0)  # Accessing the default webcam (change 0 to the appropriate index if multiple webcams are connected)

# Get the default webcam's resolution
frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create VideoWriter object
out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

# Record video for 30 seconds
record_time = 30  # Duration in seconds
start_time = cv2.getTickCount()  # Get initial time

while True:
    ret, frame = video_capture.read()
    out.write(frame)
    
    current_time = cv2.getTickCount()
    elapsed_time = (current_time - start_time) / cv2.getTickFrequency()
    
    #cv2.imshow('Recording', frame)
    
    # Break the loop if 30 seconds have elapsed
    if elapsed_time >= record_time:
        break
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and writer, and close windows
video_capture.release()
out.release()
cv2.destroyAllWindows()