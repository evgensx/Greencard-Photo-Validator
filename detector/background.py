import cv2

# Load the image
image = cv2.imread("../materials/test_input.jpg")
# image = cv2.imread("materials/img.JPG")

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold the image to create a mask of the background
ret, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

# Invert the mask to create a mask of the foreground
foreground_mask = cv2.bitwise_not(mask)

# Apply a morphological opening operation to the mask to remove small objects
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
background_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_OPEN, kernel)

# Apply the mask to the original image to extract the background
background = cv2.bitwise_and(image, image, mask=background_mask)

# Save the background image to a file
cv2.imwrite("../background.jpg", background)

# image = cv2.imread("materials/test_input.jpg")
# image = cv2.imread("materials/img.JPG")