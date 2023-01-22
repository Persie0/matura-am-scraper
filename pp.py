import PyPDF2
import re

# Loop through the pages of the PDF
def find_right_page(pdf_reader, such_string, first_match=True):
    # Initialize a variable to keep track of the number of times the string is found
    count = 0
    # Iterate through all pages
    for page_number in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page_number)
        # Extract the text from the page
        text = page.extractText()
        # Search for the string in the text
        match = re.search(such_string, text)
        if match:
            if first_match:
                return page_number+1
            else:
                count += 1
                if count == 2:
                    return page_number+1
    return pdf_reader.getNumPages()-1

        
    return such_page

# Open the PDF file
with open("pdfs/Sauna (PT3_2020)_859.pdf", "rb") as f:
    pdf_reader = PyPDF2.PdfFileReader(f)
    page_number = find_right_page(pdf_reader, "c1\)")
    if page_number != -1:
        print("String found again on page: ", page_number)
    else:
        print("String not found")