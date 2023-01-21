import json
import requests
from PIL import Image
from io import BytesIO
import pytesseract
import PyPDF2
from PIL import Image

#open beispiele.json
with open('beispiele.json') as json_file:
    data = json.load(json_file)

thema="absoluter und relativer Fehler"

#filter by thema
data = [i for i in data if i['thema'] == thema]

first = data[0]

print(first)

#get "aufgabe_body"
ab=first['aufgabe_body']

#get ab as image and ocr image
response = requests.get(ab)
img = Image.open(BytesIO(response.content))
text = pytesseract.image_to_string(img, lang='deu')
print(text)

#extract first letter + ")"
aufgabe = text.split(")")[0].trim()
print(aufgabe)

#download "loesung" as pdf
lo=first['loesung']
response = requests.get(lo)
with open('loesung.pdf', 'wb') as f:
    f.write(response.content)

pdf_file = open("loesung.pdf", "rb")
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

pdf_file[99]

start_string = "start of image"
end_string = "end of image"
start_coords = None
end_coords = None
start_page = None
end_page = None

# Loop through the pages of the PDF
for page_num in range(pdf_reader.numPages):
    page = pdf_reader.getPage(page_num)
    text = page.extractText()
    layout = page.getPageLayout()
    start_index = text.find(start_string)
    end_index = text.find(end_string)
    if start_index != -1:
        # start string found
        start_coords = layout[start_string]
        start_page = page_num
    if end_index != -1:
        # end string found
        end_coords = layout[end_string]
        end_page = page_num

if start_coords is not None and end_coords is not None:
    # Both strings were found
    if start_page == end_page:
        # Strings are on the same page
        image_data = pdf_reader.getPage(start_page).extractImage()
        cropped_image = Image.open(image_data).crop((start_coords[0], start_coords[1], end_coords[0], end_coords[1]))
    else:
        # Strings are on different pages
        start_image_data = pdf_reader.getPage(start_page).extractImage()
        start_image = Image.open(start_image_data)
        start_cropped_image = start_image.crop((start_coords[0], start_coords[1], start_image.width, start_image.height))

        end_image_data = pdf_reader.getPage(end_page).extractImage()
        end_image = Image.open(end_image_data)
        end_cropped_image = end_image.crop((0, 0, end_coords[0], end_coords[1]))

        # Create a new image and paste the two cropped images
        cropped_image = Image.new("RGB", (start_image.width + end_image.width, max(start_image.height, end_image.height)))
        cropped_image.paste(start_cropped_image, (0, 0))
        cropped_image.paste(end_cropped_image, (start_image.width, 0))
    cropped_image.save("cropped_image.png")
else:
    print("Both strings not found")


pdf_file.close()



