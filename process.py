import cv2
import imutils
import numpy as np
import pytesseract

from collections import Counter

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


plate_list = []
son_plaka = ""


#while(cap.isOpened()):

def procces(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)
    #thr1 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    ret, thr1 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    edged = cv2.Canny(thr1, 100, 255)  # Perform Edge detection
    #cv2.imshow("thr", edged)
    #cv2.waitKey(100)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:50]
    screenCnt = None
    # loop over our contours
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
        break
    if screenCnt is None:
        detected = 0
    else:
        detected = 1
    '''if detected == 1:
        cv2.drawContours(frame, [screenCnt], -1, (255, 255, 255), 2)'''
    return frame, screenCnt, detected

def pre_proc(frame):
    frame, screenCnt, detected = procces(frame)
    return frame, screenCnt,detected

def test_text(plate_text):
    chars_numbers = "0123456789 ABCDEFGHIJKLMNOPRSTUVYZ"
    chars_numbers_list = list(chars_numbers)
    plate_text_list = list(plate_text)
    x = 0
    y = 1
    if len(plate_text) > 3:
        for c in plate_text_list:
            if c not in chars_numbers_list:
                y = 0
        x = 1
    if x == 1 and y == 1:
        return True

def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0:][0]

def reading(frame, screenCnt):
    global plate_list
    global son_plaka
    crd = screenCnt[0]
    x0, y0 = crd[0]
    crd = screenCnt[1]
    x1, y1 = crd[0]
    crd = screenCnt[2]
    x2, y2 = crd[0]
    crd = screenCnt[3]
    x3, y3 = crd[0]
    pts = np.array([(x0, y0), (x1, y1), (x2, y2), (x3, y3)], dtype="float32")
    Cropped = four_point_transform(frame, pts)

    #Cropped = cv2.fastNlMeansDenoisingColored(Cropped, None, 10, 10, 7, 15)
    Cropped = cv2.cvtColor(Cropped, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(Cropped, ksize=(3, 3), sigmaX=0)
    ret, Cropped = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #cv2.imshow('Cropped', Cropped)
    #cv2.imshow('frame', frame)
    #cv2.waitKey(100)
    try:
        text = pytesseract.image_to_string(Cropped, config='--psm 7')
    except:
        print("hata")

    if test_text(text):
        text = text.replace(" ", "")
        plate_list.append(text)
        a = int(most_frequent(plate_list)[1])
        if a > 4:
            if son_plaka != most_frequent(plate_list)[0]:
                son_plaka = most_frequent(plate_list)[0]
                #print("Detected Number is:", most_frequent(plate_list)[0])
                PlateText = most_frequent(plate_list)[0]
                PlateCrop = blur
                return PlateText, PlateCrop
            plate_list = []

    return None, None



def order_points(pts):

	rect = np.zeros((4, 2), dtype = "float32")

	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]

	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	'''rect[0] = rect[0] - 5
	rect[1] = rect[1] - 5
	rect[2] = rect[2] + 5
	rect[3] = rect[3] + 5'''

	return rect

def four_point_transform(image, pts):

	rect = order_points(pts)
	(tl, tr, br, bl) = rect


	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))


	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))


	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")

	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))


	return warped
