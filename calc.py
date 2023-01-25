import cv2
import json
import sys
sys.path.append('/usr/local/lib/python3.8/dist-packages')
import requests
from PIL import Image
from io import BytesIO
import PyPDF2
import os
from pdf2image import convert_from_path
import re
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdf2image import convert_from_path
from PIL import Image
import numpy as np

def find_grey_rectangle(img_name):
    # Load the image
    img = cv2.imread(img_name)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    # add white color an all borders
    #img = cv2.copyMakeBorder(img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    


    # Find all the contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the contours by their y-coordinate
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])

    # Iterate through all the contours
    for cnt in contours:
        # Find the bounding rect of the contour
        x, y, w, h = cv2.boundingRect(cnt)
        # Filter the contours based on their area and width, and if height is not less than 10% of the image height
        # (to filter out small contours that might be noise)
        if w >= 0.75*img.shape[1] and h >= 0.1*img.shape[0]:
            #check if the rectangle is not the whole image
            if x > 0 and y > 0 and x+w < img.shape[1] and y+h < img.shape[0]:
                #cut the image so only the rectangle is left
                img = img[y:y+h, x:x+w]
                break


    # Convert the cropped image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    # Find the non-zero pixels in the thresholded image
    non_zero_pixels = cv2.findNonZero(thresh)

    # Get the bounding rectangle of the non-zero pixels
    (x, y, w, h) = cv2.boundingRect(non_zero_pixels)

    # Add some padding to the bounding rectangle
    x -= 10
    y -= 10
    w += 20
    h += 20

    #error handling
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    if x+w > img.shape[1]:
        w = img.shape[1] - x
    if y+h > img.shape[0]:
        h = img.shape[0] - y

    # Crop the image using the bounding rectangle coordinates
    img = img[y:y+h, x:x+w]

    # Save the cropped image
    cv2.imwrite("img_name.png", img)

find_grey_rectangle('113a_loesung (1).jpeg')