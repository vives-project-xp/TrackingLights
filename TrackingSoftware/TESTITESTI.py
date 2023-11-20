import cv2

def test_camera():
    # Initialize video capture
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Display the original frame
        cv2.imshow('Original Frame', frame)

        # Resize the framexcd
        width = 400
        height = 300
        resized_frame = cv2.resize(frame, (width, height))

        # Display the resized frame
        cv2.imshow('Resized Frame', resized_frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_camera()
