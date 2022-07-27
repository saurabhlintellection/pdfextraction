from pdf2image import convert_from_path
import os
import sys
import time

outputDir = "images/"
number_of_pages_to_convert = 1

def convert(file, outputDir):

    outputDir = outputDir + str(round(time.time())) + '/'
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    pages = convert_from_path(file, 500)
    counter = 1
    for page in pages:
        if counter > number_of_pages_to_convert:
            print('just one page')
            break
        
        myfile = outputDir +'output' + str(counter) +'.jpg'
        print(myfile)
        
        counter = counter + 1
        page.save(myfile, "JPEG")
    return outputDir


args = sys.argv
if len(args) > 1:
    file = args[1]
    new_output_dir = convert(file, outputDir)


print("Pdf has been converted into images located in: ", new_output_dir)
##################################################################################################################################################
print("Cropping images into different sections...")

from PIL import Image

image_dimensions = "4132 x 5848" #just a note

# image_to_convert = Image.open(new_output_dir + "output1.jpg")

# coordinates_for_total = { "x1": 3400,"y1":4150,"x2":3700,"y2":4400 }
# cropped_total = image_to_convert.crop((coordinates_for_total["x1"], coordinates_for_total["y1"], coordinates_for_total["x2"], coordinates_for_total["y2"]))
# cropped_total.show()

# coordinates_for_part_no = { "x1": 3200,"y1":220,"x2":3700,"y2":530 }
# cropped_part_no = image_to_convert.crop((coordinates_for_part_no["x1"], coordinates_for_part_no["y1"], coordinates_for_part_no["x2"], coordinates_for_part_no["y2"]))
# cropped_part_no.show()

# coordinates_for_start_no = { "x1": 180,"y1":4050,"x2":700,"y2":4400 }
# cropped_start_no = image_to_convert.crop((coordinates_for_start_no["x1"], coordinates_for_start_no["y1"], coordinates_for_start_no["x2"], coordinates_for_start_no["y2"]))
# cropped_start_no.show()

# coordinates_for_end_no = { "x1": 650,"y1":4050,"x2":1400,"y2":4400 }
# cropped_end_no = image_to_convert.crop((coordinates_for_end_no["x1"], coordinates_for_end_no["y1"], coordinates_for_end_no["x2"], coordinates_for_end_no["y2"]))
# cropped_end_no.show()

#################################################################################################################################################
#Implementing OCR
# Import required packages

import cv2
import pytesseract

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = 'D:/Dummy_C_drive/tesseract_OCR/tesseract.exe'

# Read image from which text needs to be extracted
img = cv2.imread(new_output_dir + "output1.jpg")
# img = cropped_start_no
# Preprocessing the image starts
end_no = img[4050:4400, 680:1370]
start_no = img[4050:4400, 180:700]
part_no = img[220:530, 3200:3700]
total = img[4050:4400, 3400:3700]

def perform_ocr(image_input, data_name):
    cv2.imshow("Cropped Image", image_input)
    cv2.waitKey(0)
    # Convert the image to gray scale
    gray = cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (400, 400))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_NONE)

    # Creating a copy of image
    im2 = image_input.copy()

    # A text file is created and flushed
    file = open(data_name + ".txt", "w+")
    file.write("")
    file.close()

    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]
        
        # Open the file in append mode
        file = open(data_name + ".txt", "a")
        
        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)
        
        # Appending the text into file
        file.write(text)
        file.write("\n")
        
        # Close the file
        file.close

perform_ocr(part_no, "part_no")
perform_ocr(start_no, "start_no")
perform_ocr(end_no, "end_no")
perform_ocr(total, "total")