import PyPDF2
import re

# Open the PDF file
with open('Oelbohrungen_261.pdf', 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)

    # Iterate over each page
    for page in range(pdf_reader.numPages):
        pdf_page = pdf_reader.getPage(page)
        text = pdf_page.extractText()
    
        # Compile the regular expression
        pattern = re.compile(r'\b(?P<previous>\S+)\s+(?P<target>Berechnen Si.+?)\b')
        print(text)

        # Iterate over each match
        for match in pattern.finditer(text):
            # Compile the regular expression
            pattern2 = re.compile(r'[a-z]1\)|[a-z]\)')

            # Iterate over each match
            for match2 in pattern2.finditer(match.group('previous')):
                print(match2.group(0).strip()[:-1])
