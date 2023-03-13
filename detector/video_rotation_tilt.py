import cv2
import numpy as np

# Load the face and eye cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the face in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Iterate over each detected face
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Crop the face region from the frame
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Detect the eyes in the face region
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=2)

        # Compute the angle of the head
        eyes_center = None
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            if eyes_center is None:
                eyes_center = np.array([ex+ew/2, ey+eh/2])
            else:
                eyes_center += np.array([ex+ew/2, ey+eh/2])
        if eyes_center is not None:
            eyes_center /= len(eyes)
            dx, dy = eyes_center[0] - w/2, eyes_center[1] - h/2
            angle = np.arctan2(dy, dx) * 180 / np.pi

            # Draw the angle of the head
            cv2.putText(frame, f"Head Angle: {angle:.2f}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 0), 1)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
