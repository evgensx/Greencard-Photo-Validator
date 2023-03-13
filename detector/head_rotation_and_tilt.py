import cv2
import numpy as np

# Load the face and eye cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Load the image
img = cv2.imread("../materials/img.JPG")
# img = cv2.imread('../materials/test_input.jpg')
# img = cv2.imread("../materials/DSC_0022.jpg")

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect the face in the image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# Iterate over each detected face
for (x, y, w, h) in faces:
    # Draw a rectangle around the face
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Crop the face region from the image
    roi_gray = gray[y:y + h, x:x + w]
    roi_color = img[y:y + h, x:x + w]

    # Detect the eyes in the face region
    eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5)

    # Compute the angle of the head
    eyes_center = None
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        if eyes_center is None:
            eyes_center = np.array([ex + ew / 2, ey + eh / 2])
        else:
            eyes_center += np.array([ex + ew / 2, ey + eh / 2])
    if eyes_center is not None:
        eyes_center /= len(eyes)
        dx, dy = eyes_center[0] - w / 2, eyes_center[1] - h / 2
        angle = np.arctan2(dy, dx) * 180 / np.pi

        # Draw the angle of the head
        cv2.putText(img, f"Head Angle: {angle:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
