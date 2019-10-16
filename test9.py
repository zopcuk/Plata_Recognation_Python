import cv2
import imutils
import numpy as np
import pytesseract
from pyimagesearch.transform import four_point_transform
from collections import Counter

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


#cap = cv2.VideoCapture("2.mp4")
cap = cv2.VideoCapture("9102_Trim.mp4")
plate_list = []
son_plaka = ""
while(cap.isOpened()):

    ret, FrameOrigin = cap.read()
    frame = FrameOrigin
    def procces(frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)
        edged = cv2.Canny(blur, 30, 200)  # Perform Edge detection
        cv2.imshow('closing', edged)
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
    frame, screenCnt, detected = procces(frame)
    if detected == 1:
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
        cv2.imshow('Cropped', Cropped)
        cv2.imshow('frame', frame)
        cv2.waitKey(100)
        try:
            text = pytesseract.image_to_string(Cropped, config='--psm 13')
            #text = pytesseract.image_to_string(Cropped, config='--psm 7 -c tessedit_char_whitelist=0123456789ABCÇDEFGHIİJKLMNOÖPRSŞTUÜVYZX')
        except:
            print("hata")
#############################
        def test_text(plate_text):
            chars_numbers = "0123456789 ABCDEFGHIJKLMNOPRSTUVYZ"
            chars_numbers_list = list(chars_numbers)
            plate_text_list = list(plate_text)
            x = 0
            y = 1
            if len(plate_text) > 4:
                for c in plate_text_list:
                    if c not in chars_numbers_list:
                        y = 0
                x = 1
            if x == 1 and y == 1:
                return True
####################################

        def most_frequent(List):
            occurence_count = Counter(List)
            return occurence_count.most_common(1)[0:][0]
        if test_text(text):
            text = text.replace(" ", "")
            plate_list.append(text)
            a = int(most_frequent(plate_list)[1])
            if a > 5:
                if son_plaka != most_frequent(plate_list)[0]:
                    son_plaka = most_frequent(plate_list)[0]
                    print("Detected Number is:", most_frequent(plate_list)[0])
                plate_list = []
        else:
            detected = 0

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
