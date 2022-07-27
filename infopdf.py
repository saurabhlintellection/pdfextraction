from PyPDF2 import PdfReader

reader = PdfReader("U05A1P1Un.pdf")
number_of_pages = len(reader.pages)
print("number of pages", number_of_pages)
page = reader.pages[0]
print(page)
text = page.extract_text()

print ("extracted text: ", text)

# import PyPDF2

# a = PyPDF2.PdfFileReader('U05A1P1.pdf')
# if a.isEncrypted:
#     a.decrypt('')
# print(a.documentInfo)
# number_of_pages = len(a.pages)
# print("number of pages", number_of_pages)
# page = a.pages[0]
# # text = page.extract_text()


# print ("extracted text: ",a.getPage(2).extract_text())

# from pdfminer import high_level

# local_pdf_filename = "U05A1P1Un.pdf"
# pages = [0] # just the first page
# extracted_text = high_level.extract_text(local_pdf_filename, "", pages)
# print(extracted_text)