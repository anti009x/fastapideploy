import cv2 as cv
import numpy as np
from scipy.spatial.distance import euclidean
from imutils import perspective

def box_model(img, pixel_per_cm):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
    gray = cv.dilate(gray, None, iterations=2)
    gray = cv.erode(gray, None, iterations=1)

    # Apply thresholding on the gray image to create a binary image
    ret, thresh = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
    
    # Find the contours
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    if contours:
            # Take the largest contour based on area
            cnt = max(contours, key=cv.contourArea)
            # Filter contours that are significant in size
            contours = [cnt for cnt in contours if cv.contourArea(cnt) > 500 and cv.arcLength(cnt, True) > 100]
            if not contours:
                return img, None, None  # Return None if no significant contours are found
            
            cnt = contours[0]  # Use the first significant contour
            box = cv.minAreaRect(cnt)
            box = cv.boxPoints(box)
            box = np.array(box, dtype="int")
            box = perspective.order_points(box)
            (tl, tr, br, bl) = box
            
            # Calculate width and height using the calibrated pixel_per_cm
            wid = euclidean(tl, tr) / pixel_per_cm
            ht = euclidean(tr, br) / pixel_per_cm
            
            # Compute the bounding rectangle of the contour
            x, y, w, h = cv.boundingRect(cnt)
            
            # Draw the contour and bounding rectangle
            img = cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            return img, wid, ht
    return img, None, None