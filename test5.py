import cv2
import imutils
import numpy as np
import pytesseract
from pyimagesearch.transform import four_point_transform



pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


cap = cv2.VideoCapture('2.mp4')

while(cap.isOpened()):

    ret, frame = cap.read()

    '''(h, w) = frame.shape[:2]
    # calculate the center of the image
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, 180, 1)
    frame = cv2.warpAffine(frame, M, (w, h))'''

    def procces(frame):
        #frame = cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)
        #gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
        edged = cv2.Canny(blur, 30, 200)  # Perform Edge detection

        cv2.imshow('edged', edged)
        # find contours in the edged image, keep only the largest
        # ones, and initialize our screen contour,
        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]
        screenCnt = None
        # loop over our contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)

            # if our approximated contour has four points, then
            # we can assume that we have found our screen

            if len(approx) == 4:
                screenCnt = approx
            break

        if screenCnt is None:
            detected = 0
            print("No contour detected")
        else:
            detected = 1

        if detected == 1:
            cv2.drawContours(frame, [screenCnt], -1, (255, 255, 255), 3)
        return gray, frame, screenCnt, detected

    gray, frame, screenCnt, detected = procces(frame)

    if detected == 1:
        '''        #frame = imutils.rotate(frame, 20)   ROTATE
        #gray = imutils.rotate(gray, 30)

        # Masking the part other than the number plate
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
        new_image = cv2.bitwise_and(frame, frame, mask=mask)


        # Now crop
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = frame[topx:bottomx + 1, topy:bottomy + 1]'''

        crd = []
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


        hsv = cv2.cvtColor(Cropped, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        Cropped[mask > 0] = (255, 255, 255)
        Cropped = cv2.cvtColor(Cropped, cv2.COLOR_BGR2GRAY)
        Cropped = cv2.GaussianBlur(Cropped, ksize=(9, 9), sigmaX=0, sigmaY=0)
        ret, Cropped = cv2.threshold(Cropped, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)



        # Read the number plate
        text = ""
        try:
            text = pytesseract.image_to_string(Cropped, config='--psm 12')
            #text = pytesseract.image_to_string(Cropped, config='--psm 7 -c tessedit_char_whitelist=0123456789ABCÇDEFGHIİJKLMNOÖPRSŞTUÜVYZX')
        except:
            print("hata")

        #text = pytesseract.image_to_string(Cropped, config='--psm 7 -c tessedit_char_whitelist=0123456789ABCÇDEFGHIİJKLMNOÖPRSŞTUÜVYZX')
        #chars = '!^+%&/()=?-><|/*-+>£#$½{[]}\*.,;:'   any((c in chars) for c in text)
        if len(text) > 0:
            print("Detected Number is:", text)
            cv2.imshow('image', frame)
            cv2.imshow('Cropped', Cropped)

            cv2.waitKey(0)
            cv2.destroyAllWindows()

        else:
            detected = 0




    cv2.imshow('frame',gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()