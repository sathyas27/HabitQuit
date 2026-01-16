import cv2

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream or file.")
    exit()
else:
    print("Camera opened successfully!")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If the frame is read correctly, ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Display the resulting frame
    cv2.imshow('Mac Camera Feed', frame)

    # Press 'q' on the keyboard to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture object and destroy all windows
cap.release()
cv2.destroyAllWindows()