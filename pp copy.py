from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdf2image import convert_from_path
from PIL import Image

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
                for element in layout:
                    if hasattr(element,'get_text'):
                        if string in element.get_text().strip():
                            if  firs:
                                firs=False
                                pz = element.bbox[1]/layout.height
                                # Convert the page to an image
                                images = convert_from_path(pdf_file, first_page=page_number, last_page=page_number)
                                image = images[0]
                                p2=image.height
                            else:
                                p2 = element.bbox[1]/layout.height


                            # Crop the image based on the y value
                image = image.crop((0, image.height-pz*image.height-70, image.width, image.height-p2*image.height-50))
                return image
    return None

pdf_file = "pdfs/A_310 Erkaeltung (PT3_2021)_899.pdf"
string = "a1)"
page_number = 3
image = get_string_position_and_crop(pdf_file, string, page_number)
if image:
    image.show()
else:
    print(f"The string '{string}' was not found on page {page_number}.")
