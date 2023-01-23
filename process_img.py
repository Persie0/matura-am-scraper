import cv2

# Load the image
img = cv2.imread("/home/perzi/Downloads/matura am scraper/775d_loesung.jpeg")

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply thresholding
ret, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

# Find all the contours
contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Sort the contours by their y-coordinate
contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])

# Iterate through all the contours
cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
for cnt in contours:
    # Find the bounding rect of the contour
    x, y, w, h = cv2.boundingRect(cnt)
    # Filter the contours based on their area and width
    if w >= 0.75*img.shape[1]:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        break

#cut the image so only the rectangle is left
img = img[y:y+h, x:x+w]

# save the image
cv2.imwrite("936bb_loesung.jpeg", img)