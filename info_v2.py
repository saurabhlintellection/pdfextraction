import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io    


def pdfparser(data):
    fp = open(data, 'rb')      
    rsrcmgr = PDFResourceManager()
    # retstr = io.StringIO() #This will cause -- `TypeError: unicode argument expected, got 'str'`
    retstr = io.BytesIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)

    data = retstr.getvalue() #Indentation was worng here
    fp.close()
    #print(data)
    return data


if __name__ == '__main__':
    #PDF file you provied is encrypted with blank password, we need to decrypt it
    path = sys.argv[0]
    from subprocess import call
    import os
    pdf_filename = os.path.basename(path)
    file_name, extension = os.path.splitext(pdf_filename)
    pdf_filename_decr = str(file_name) + "_decr" + extension
    call('qpdf --password=%s --decrypt %s %s' %('', path, pdf_filename_decr), shell=True)

    text = pdfparser("U05A1P1Un.pdf")