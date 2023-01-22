import json
import requests
from PIL import Image
from io import BytesIO
import pytesseract
import PyPDF2
from PIL import Image
import os
from pdf2image import convert_from_path
import easyocr
import re

#open themen.json
with open('themen.json') as json_file:
    themen = json.load(json_file)


#open beispiele.json
with open('beispiele.json') as json_file:
    data = json.load(json_file)

for the in themen:
    thema=the["thema"]

    #filter by thema
    data = [i for i in data if i['thema'] == thema]

    #if no thema folder make one
    if not os.path.exists(thema):
        os.makedirs(thema)

        #if no thema folder make one
    if not os.path.exists("pdfs"):
        os.makedirs("pdfs")


    for bsp in data:
        aufgabe_name= bsp["name"]+"_"+bsp["id"]

        auf_dir=thema+"/"+aufgabe_name
        if os.path.exists(auf_dir+"/"+"loesung.jpeg"):
            continue
        
        #get "aufgabe_body"
        ab=bsp['aufgabe_body']

        #get ab as image and ocr image
        response = requests.get(ab)
        img = Image.open(BytesIO(response.content))
        

        #ocr image with easyocr
        reader = easyocr.Reader(['de'], gpu=False)
        result = reader.readtext(img)
        text = result[0][1]
        
        #download "loesung" as pdf
        loe=bsp['loesung']
        pdf_name= aufgabe_name+".pdf"
        #check if already downloaded
        if not os.path.exists("pdfs/"+pdf_name):
            r = requests.get(loe, allow_redirects=True)
            open("pdfs/"+pdf_name, 'wb').write(r.content)

        #extract bsp letter + ")"
        aufgabe = text.split(")")[0].strip()

        pdf_file = open("pdfs/"+pdf_name, "rb")
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        if len(aufgabe) > 5:
            #find text before aufgabe   
            for i in range(pdf_reader.numPages):
                page = pdf_reader.getPage(i)
                page_text = page.extractText()
                if aufgabe in page_text:
                    #get index of aufgabe
                    index = page_text.index(aufgabe[:12])
                    au=page_text[index-10:index]
                    kk=au.strip().split(" ")[-1]
                    print(kk)

            





            #path to downloaded pdf
            pdf_path = "pdfs/"+pdf_name
            print(pdf_path)
            aufgabe = input("Aufgabe: ")

        #make aufgabe_name directory in thema dir
        if not os.path.exists(auf_dir):
            os.makedirs(auf_dir)
        
        #download "aufgabe_head" as image
        ah=bsp['aufgabe_head']
        ah_name= aufgabe_name+"_ah"
        ah_path= auf_dir+"/"+ah_name+".png"
        #check if already downloaded
        if not os.path.exists(ah_path):
            response = requests.get(ah)
            img = Image.open(BytesIO(response.content))
            img.save(ah_path)

        #download "aufgabe_body" as image
        ab=bsp['aufgabe_body']
        ab_name= aufgabe_name+"_ab"
        ab_path= auf_dir+"/"+ab_name+".png"
        #check if already downloaded
        if not os.path.exists(ab_path):
            response = requests.get(ab)
            img = Image.open(BytesIO(response.content))
            img.save(ab_path)
        
        #extract solution

        such_string = aufgabe+"1)"
        print(such_string)
        such_page = None

        # Loop through the pages of the PDF
        def find_right_page(pdf_reader, such_string):
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text = page.extractText()
            #if second time found such_string, break
                con=0
                con2=0
            #check count how often such_string in text, check if lösung - bewertungschlüssel on one page
                for i in range(len(text)):
                    if text[i:i+len(such_string)] == such_string:
                        con+=1
                    #if second time found such_string, break
                        if con == 2:
                            such_page = page_num
                            break
            #if not found, check if such_string in text, qst is aufgabe, 2nd läsung
                if such_string in text:
                    such_page = page_num
                    break
            return such_page
        print(such_string)
        such_page = find_right_page(pdf_reader, such_string)


        if such_page is None:
            such_string = aufgabe+")"
            such_page = find_right_page(pdf_reader, such_string)

            

        if such_page is not None:
            #save page as image
            pages = convert_from_path("pdfs/"+pdf_name)
            pages[such_page].save(auf_dir+"/"+"loesung.jpeg", 'JPEG')
            # Open the image
            im = Image.open(auf_dir+"/"+"loesung.jpeg")

            # Define the crop coordinates
            left = 0
            top = 0
            right = im.width
            bottom = im.height
            
            # Find the index of the desired string
            # Get the bounding box coordinates for each character in the string
            boxes = pytesseract.image_to_boxes(im, lang='deu')
            whole_string = ""
            ind=0
            for b in boxes.splitlines():
                whole_string += b.split(' ')[0]
                if such_string in whole_string and top == 0:
                    ind=len(whole_string)-1
                    # Get the bounding box coordinates
                    b = b.split(' ')
                    top = im.height - int(b[2]) - 50
                    if top <= 0:
                        top = 1
                #if such_string is two times in text, break
                if such_string in whole_string[ind+1:] and ind!=0:
                    b = b.split(' ')
                    pos2 = int(b[2])
                    bottom = im.height - int(b[2]) - 40
                    break

            # Crop the image
            cropped_im = im.crop((left, top, right, bottom))

            # Save the cropped image
            cropped_im.save(auf_dir+"/"+"loesung.jpeg")
        else:
            print(loe)
            
        pdf_file.close()



