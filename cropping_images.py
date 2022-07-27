# from PIL import Image

# image_dimensions = "4132 x 5848" #just a note

# image_to_convert = Image.open("./images/1653910485/output1.jpg")

# coordinates_for_start_no = { "x1": 650,"y1":4050,"x2":1400,"y2":4400 }

# cropped_start_no = image_to_convert.crop((coordinates_for_start_no["x1"], coordinates_for_start_no["y1"], coordinates_for_start_no["x2"], coordinates_for_start_no["y2"]))

# cropped_start_no.show()
# print(type(cropped_start_no))

# Import required packages
import cv2
import pytesseract

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = 'D:/Dummy_C_drive/tesseract_OCR/tesseract.exe'

# Read image from which text needs to be extracted
img = cv2.imread("./images/1653910485/output1.jpg")
# img = cropped_start_no
# Preprocessing the image starts
start_no = img[4050:4400, 680:1370]
cv2.imshow("Starting Serial Number", start_no)
cv2.waitKey(0)
# Convert the image to gray scale
gray = cv2.cvtColor(start_no, cv2.COLOR_BGR2GRAY)

# Performing OTSU threshold
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

# Specify structure shape and kernel size.
# Kernel size increases or decreases the area
# of the rectangle to be detected.
# A smaller value like (10, 10) will detect
# each word instead of a sentence.
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (200, 200))

# Applying dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

# Finding contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
												cv2.CHAIN_APPROX_NONE)

# Creating a copy of image
im2 = start_no.copy()

# A text file is created and flushed
file = open("recognized.txt", "w+")
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
	file = open("recognized.txt", "a")
	
	# Apply OCR on the cropped image
	text = pytesseract.image_to_string(cropped)
	
	# Appending the text into file
	file.write(text)
	file.write("\n")
	
	# Close the file
	file.close
