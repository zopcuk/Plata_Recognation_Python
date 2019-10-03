import math
import cv2
import imutils
import numpy as np
import pytesseract
import re
#from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


cap = cv2.VideoCapture('2.mp4')


while(cap.isOpened()):

    ret, frame = cap.read()

    angle = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, ksize=(7, 7), sigmaX=0)
    #gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
    edged = cv2.Canny(blur, 30, 200)  # Perform Edge detection
    cv2.imshow('edged', edged)
    # find contours in the edged image, keep only the largest
    # ones, and initialize our screen contour,
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:50]
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
            crd = []
            crd = approx[0]
            x1, y1 = crd[0]
            crd = approx[2]
            x2, y2 = crd[0]
            angle = math.tanh((x1-x2)/(y2-y1))

        break


    if screenCnt is None:
        detected = 0
        print("No contour detected")
    else:
        detected = 1

    if detected == 1:
        cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 3)

    if detected == 1:
        #frame = imutils.rotate(frame, 20)   ROTATE
        #gray = imutils.rotate(gray, 30)

        # Masking the part other than the number plate
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
        new_image = cv2.bitwise_and(frame, frame, mask=mask)


        # Now crop
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]
        # Read the number plate
        text = pytesseract.image_to_string(Cropped, config='--psm 7')
        #text = pytesseract.image_to_string(Cropped, config='-c preserve_interword_spaces=1 tessedit_char_whitelist=0123456789ABCÇDEFGHIİJKLMNOÖPRSŞTUÜVYZX --psm 7')
        #chars = '!^+%&/()=?-><|/*-+>£#$½{[]}\*.,;:'
        if len(text) > 5:
            print("Detected Number is:", text)
        else:
            detected = 0

        cv2.imshow('image', frame)

        cv2.imshow('Cropped', Cropped)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    cv2.imshow('frame',gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()