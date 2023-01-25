#download and extract images

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
    ret, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

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
    cv2.imwrite(img_name, img)


# Loop through the pages of the PDF
def find_right_page(pdf_reader, such_string, first_match=True):
    # Initialize a variable to keep track of the number of times the string is found
    count = 0
    # Iterate through all pages
    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]
        # Extract the text from the page
        text = page.extract_text()
        # Search for the string in the text
        match = re.search(such_string, text)
        if match:
            if first_match:
                return page_number+1
            else:
                count += 1
                if count == 2:
                    return page_number+1
    return -1
    
def get_string_position_and_crop(pdf_file, string, page_number):
    print("suche nach: "+string+ ", seite: " + str(page_number) + ", in: "+pdf_file)
    with open(pdf_file, 'rb') as f:
        # Create a PDF resource manager object that stores shared resources
        resource_manager = PDFResourceManager()
        # Create a PDF page aggregator object
        device = PDFPageAggregator(resource_manager, laparams=LAParams())
        # Create a PDF interpreter object
        interpreter = PDFPageInterpreter(resource_manager, device)
        # Process the specific page
        for i, page in enumerate(PDFPage.get_pages(f)):
            if i == page_number-1:
                interpreter.process_page(page)
                # Receive the LTPage object for the page
                layout = device.get_result()
                # Iterate through the layout elements
                firs=True
                pz=1
                images = convert_from_path(pdf_file, first_page=page_number, last_page=page_number)
                image = images[0]
                p2=image.height
                for element in layout:
                    if hasattr(element,'get_text'):
                        if string in element.get_text().strip():
                            print(element.get_text().strip())
                            if firs:
                              print(element.bbox[1]/layout.height)
                              firs=False
                              pz = element.bbox[1]/layout.height
                              # Convert the page to an image
                                
                                
                            else:
                                p2 = element.bbox[1]/layout.height
                                p2=image.height-p2*image.height-50

                # Crop the image based on the y value
                y1=image.height-pz*image.height-80
                if (y1) < 0:
                  y1=0
               # Handle the case where the crop parameters are outside the image
                if p2 > image.height:
                  p2=image.height
                try:
                  image = image.crop((0, y1, image.width, p2))
                  image.save(auf_dir+"/"+bsp["id"]+aufgabe+"_loesung.jpeg")
                except:
                  try:
                    image = image.crop((0, image.height, image.width, p2))
                    image.save(auf_dir+"/"+bsp["id"]+aufgabe+"_loesung.jpeg")
                  except:
                    print("Not cropped: "+ pdf_file)
    return None

#open themen.json
with open("/content/drive/MyDrive/"+'themen.json') as json_file:
    themen = json.load(json_file)

if not os.path.exists("/content/drive/MyDrive/Themen/"):
  os.makedirs("/content/drive/MyDrive/Themen/")
      #if no thema folder make one
if not os.path.exists("/content/drive/MyDrive/pdfs"):
    os.makedirs("/content/drive/MyDrive/pdfs")

for the in themen:
  #open beispiele.json
  with open("/content/drive/MyDrive/"+'beispiele.json') as json_file:
      data = json.load(json_file)
  thema=the["thema"]
  print(thema)


  #filter by thema
  data = [i for i in data if i['thema'] == thema]



  for bsp in data:
          #get "aufgabe_body"
      ab=bsp['aufgabe_body']
       #extract bsp letter + ")"
      aufgabe = ab.split("/")[-1].split(".")[0]
      aufgabe_name= bsp["name"]+"_"+bsp["id"]+aufgabe

      auf_dir="/content/drive/MyDrive/Themen/"+thema+"/"+aufgabe_name

      #if os.path.exists(auf_dir+"/"+bsp["id"]+aufgabe+"_loesung.jpeg"):
          #continue
      
      #download "loesung" as pdf
      loe=bsp['loesung']
      pdf_name= bsp["name"]+"_"+bsp["id"]+".pdf"
      #check if already downloaded
      if not os.path.exists("/content/drive/MyDrive/"+"pdfs/"+pdf_name):
          r = requests.get(loe, allow_redirects=True)
          open("/content/drive/MyDrive/"+"pdfs/"+pdf_name, 'wb').write(r.content)

     


      pdf_file = open("/content/drive/MyDrive/"+"pdfs/"+pdf_name, "rb")
      pdf_reader = PyPDF2.PdfReader(pdf_file)


      #make aufgabe_name directory in thema dir
      if not os.path.exists(auf_dir):
          os.makedirs(auf_dir)
      
      #download "aufgabe_head" as image
      ah=bsp['aufgabe_head']
      ah_name= bsp["id"]+aufgabe+"_ah"
      ah_path= auf_dir+"/"+ah_name+".png"
      #check if already downloaded
      if not os.path.exists(ah_path):
          response = requests.get(ah)
          img = Image.open(BytesIO(response.content))
          img.save(ah_path)

      #download "aufgabe_body" as image
      ab=bsp['aufgabe_body']
      ab_name= bsp["id"]+aufgabe+"_ab"
      ab_path= auf_dir+"/"+ab_name+".png"
      #check if already downloaded
      if not os.path.exists(ab_path):
          response = requests.get(ab)
          img = Image.open(BytesIO(response.content))
          img.save(ab_path)
      
      #extract solution

      such_string = aufgabe+"1)"
      reg=aufgabe+"1\)"
      such_page = None



      
      print(pdf_file)
      such_page = find_right_page(pdf_reader, reg, True)


      if such_page == -1:
          such_string = aufgabe+")"
          reg=aufgabe+"\)"
          such_page = find_right_page(pdf_reader, reg, False)

      if such_page == -1:
        such_page=len(pdf_reader.pages)-1

          

      image = get_string_position_and_crop("/content/drive/MyDrive/"+"pdfs/"+pdf_name, such_string, such_page)
      find_grey_rectangle(auf_dir+"/"+bsp["id"]+aufgabe+"_loesung.jpeg")
      
          
      pdf_file.close()
      print("\n\n")



