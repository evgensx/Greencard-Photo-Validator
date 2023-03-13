import cv2
import numpy as np

k = 0

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
img = cv2.imread("../materials/img.JPG")
# img = cv2.imread('../materials/test_input.jpg')
# img = cv2.imread("../materials/DSC_0022.jpg")
# img = cv2.imread("../CROPPED-photo_2023-03-04_19-16-44_cr.jpg")
# img = cv2.imread("../shadow.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect the faces in the image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Iterate through the detected faces and check for shadows
for (x, y, w, h) in faces:
    roi_gray = gray[y:y + h, x:x + w]
    _, thresh = cv2.threshold(roi_gray, 127, 255, cv2.THRESH_BINARY_INV)

    # Remove the definition of hair and eyes
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    thresh = cv2.erode(thresh, kernel, iterations=2)
    thresh = cv2.dilate(thresh, kernel, iterations=4)

    # Detect the edges of the face
    edges = cv2.Canny(roi_gray, 100, 200)

    # Remove the edges that are not facing the light source
    light_angle = 135  # Angle of the light source (in degrees)
    light_angle_rad = np.deg2rad(light_angle)
    cos_angle = np.cos(light_angle_rad)
    sin_angle = np.sin(light_angle_rad)
    x_center = x + w // 2
    y_center = y + h // 2
    for y_pixel in range(y, y + h):
        for x_pixel in range(x, x + w):
            if thresh[y_pixel - y, x_pixel - x] == 0:  # Exclude the definition of hair and eyes
                continue
            x_offset = x_pixel - x_center
            y_offset = y_pixel - y_center
            if x_offset * cos_angle - y_offset * sin_angle < 0:
                edges[y_pixel - y, x_pixel - x] = 0

    # Remove the definition of shadows under the eyes
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (ex, ey, ew, eh) in eyes:
        eye_mask = np.zeros(thresh.shape[:2], dtype=np.uint8)
        eye_mask[ey + y:ey + y + eh, ex + x:ex + x + ew] = 255
        contours, _ = cv2.findContours(eye_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 50:
                cv2.drawContours(thresh, [contour], -1, 0, -1)

    # Find the contours of the shadow regions
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours of the shadow regions onto the original image
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50:
            k+=1
            cv2.drawContours(img, [contour + (x, y)], -1, (0, 0, 255), 2)

#
print(k)

# Display the image with the detected shadows
cv2.imshow('Face Shadow Detector', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
