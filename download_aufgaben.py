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
            print("match", match.group(0) )
            if first_match:
                return page_number+1
            else:
                count += 1
                if count == 2:
                    return page_number+1
    return len(pdf_reader.pages)
    
def get_string_position_and_crop(pdf_file, string, page_number):
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
                                firs=False
                                pz = element.bbox[1]/layout.height
                                # Convert the page to an image
                                
                                
                            else:
                                p2 = element.bbox[1]/layout.height
                                p2=image.height-p2*image.height-50


                            # Crop the image based on the y value
                image = image.crop((0, image.height-pz*image.height-90, image.width, p2))
                return image
    return None

#open themen.json
with open(""+'themen.json') as json_file:
    themen = json.load(json_file)

if not os.path.exists("Themen/"):
  os.makedirs("Themen/")

for the in themen:
  #open beispiele.json
  with open(""+'beispiele.json') as json_file:
      data = json.load(json_file)
  thema=the["thema"]
  print(thema)


  #filter by thema
  data = [i for i in data if i['thema'] == thema]


      #if no thema folder make one
  if not os.path.exists("pdfs"):
      os.makedirs("pdfs")


  for bsp in data:
      aufgabe_name= bsp["name"]+"_"+bsp["id"]

      auf_dir="Themen/"+thema+"/"+aufgabe_name

      if os.path.exists(auf_dir+"/"+bsp["id"]+"loesung.jpeg"):
          continue
      
      #get "aufgabe_body"
      ab=bsp['aufgabe_body']

      #get ab as image and ocr image
      response = requests.get(ab)
      img = Image.open(BytesIO(response.content))
      
      #download "loesung" as pdf
      loe=bsp['loesung']
      pdf_name= aufgabe_name+".pdf"
      #check if already downloaded
      if not os.path.exists(""+"pdfs/"+pdf_name):
          r = requests.get(loe, allow_redirects=True)
          open(""+"pdfs/"+pdf_name, 'wb').write(r.content)

      #extract bsp letter + ")"
      aufgabe = ab.split("/")[-1].split(".")[0]


      pdf_file = open(""+"pdfs/"+pdf_name, "rb")
      pdf_reader = PyPDF2.PdfReader(pdf_file)


      #make aufgabe_name directory in thema dir
      if not os.path.exists(auf_dir):
          os.makedirs(auf_dir)
      
      #download "aufgabe_head" as image
      ah=bsp['aufgabe_head']
      ah_name= bsp["id"]+"ah"
      ah_path= auf_dir+"/"+ah_name+".png"
      #check if already downloaded
      if not os.path.exists(ah_path):
          response = requests.get(ah)
          img = Image.open(BytesIO(response.content))
          img.save(ah_path)

      #download "aufgabe_body" as image
      ab=bsp['aufgabe_body']
      ab_name= bsp["id"]+"ab"
      ab_path= auf_dir+"/"+ab_name+".png"
      #check if already downloaded
      if not os.path.exists(ab_path):
          response = requests.get(ab)
          img = Image.open(BytesIO(response.content))
          img.save(ab_path)
      
      #extract solution

      such_string = aufgabe+"1)"
      reg=aufgabe+"1\)"
      print("reg: "+reg)
      such_page = None



      
      print(pdf_file)
      such_page = find_right_page(pdf_reader, reg, True)


      if such_page == -1:
          reg=aufgabe+"\)"
          such_string = aufgabe+")"
          print(reg)
          such_page = find_right_page(pdf_reader, reg, False)

      print("Page: " + str(such_page))

          

      image = get_string_position_and_crop(""+"pdfs/"+pdf_name, such_string, such_page)
      if image:
          # Save the cropped image
          image.save(auf_dir+"/"+bsp["id"]+"loesung.jpeg")
          
      pdf_file.close()



