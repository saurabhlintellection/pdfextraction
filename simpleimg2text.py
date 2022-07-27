import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'D:/Dummy_C_drive/tesseract_OCR/tesseract.exe'

img = cv2.imread("./images/1653979924/output1.jpg")

start_no = img[4050:4400, 180:700]
end_no = img[4050:4400, 680:1370]
part_no = img[340:470, 3350:3620]
total = img[4100:4450, 3400:3700]

cv2.imshow("Cropped Image", part_no)
cv2.waitKey(0)

text = pytesseract.image_to_string(part_no)

print(text)