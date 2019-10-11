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
    '''(h, w) = frame.shape[:2]
    # calculate the center of the image
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, 180, 1)
    frame = cv2.warpAffine(frame, M, (w, h))'''
    def procces(frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #blur = cv2.GaussianBlur(gray, ksize=(3, 3), sigmaX=0)
        #gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
        # apply automatic Canny edge detection using the computed median
        '''v = np.median(blur)
        sigma = 0.33
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(blur, lower, upper)'''

        ''' kernel_er = np.ones((5, 5), np.uint8)
        erosion = cv2.erode(gray, kernel_er)
        cv2.imshow('er', erosion)
        kernel_dl = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        kernel1_dl = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
        edges_dilated = cv2.morphologyEx(cv2.dilate(erosion, kernel_dl), cv2.MORPH_CLOSE, kernel1_dl)
        cv2.imshow('dil', edges_dilated)'''

        blur = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)
        edged = cv2.Canny(blur, 30, 200)  # Perform Edge detection

        kernel = np.ones((2, 2), np.uint8)
        #erosion = cv2.erode(gray, kernel, iterations=1)
        #dilation = cv2.dilate(edged, kernel, iterations=1)
        #opening = cv2.morphologyEx(edged, cv2.MORPH_OPEN, kernel)
        #closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        cv2.imshow('closing', edged)



        # find contours in the edged image, keep only the largest
        # ones, and initialize our screen contour,
        cnts = cv2.findContours(edged.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:50]

        screenCnt = None
        # loop over our contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            # if our approximated contour has four points, then
            # we can assume that we have found our screen

            if len(approx) == 4:
                screenCnt = approx
            break

        if screenCnt is None:
            detected = 0
            #print("No contour detected")
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


        '''hsv = cv2.cvtColor(Cropped, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        Cropped[mask > 0] = (255, 255, 255)'''
        #Cropped = cv2.fastNlMeansDenoisingColored(Cropped, None, 10, 10, 7, 15)
        Cropped = cv2.cvtColor(Cropped, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(Cropped, ksize=(3, 3), sigmaX=0)
        #ret, Cropped = cv2.threshold(Cropped, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        #Cropped = cv2.bitwise_not(Cropped)
        cv2.imshow('Cropped', Cropped)
        cv2.imshow('frame', frame)
        cv2.waitKey(100)


        # Read the number plate

        try:
            text = pytesseract.image_to_string(Cropped, config='--psm 13')
            #text = pytesseract.image_to_string(Cropped, config='--psm 7 -c tessedit_char_whitelist=0123456789ABCÇDEFGHIİJKLMNOÖPRSŞTUÜVYZX')
        except:
            print("hata")

        #text = pytesseract.image_to_string(Cropped, config='--psm 7 -c tessedit_char_whitelist=0123456789ABCÇDEFGHIİJKLMNOÖPRSŞTUÜVYZX')
        #chars = '!^+%&/()=?-><|/*-+>£#$½{[]}\*.,;:'   any((c in chars) for c in text)
#############################
        def test_text(plate_text):
            chars_numbers = "0123456789 ABCDEFGHIJKLMNOPRSTUVYZ"
            chars_numbers_list = list(chars_numbers)
            plate_text_list = list(plate_text)
            x = 0
            y = 1
            '''cities1 = ["01", "02", "03", "04", "05", "06", "07", "08", "09"]
            cities2 = ["{}".format(i) for i in range(10, 82)]
            first2 = plate_text[:2]'''
            if len(plate_text) > 4:
                '''for c in cities1:
                    if c == first2:
                        x = 1
                for c in cities2:
                    if c == first2:
                        x = 1'''
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
            if a > 10:

                if son_plaka != most_frequent(plate_list)[0]:
                    son_plaka = most_frequent(plate_list)[0]
                    print("Detected Number is:", most_frequent(plate_list)[0])
                    #cv2.imshow('image', frame)
                    cv2.imshow('Cropped', Cropped)
                    #cv2.waitKey(100)
                    '''cv2.destroyAllWindows()'''
                plate_list = []
        else:
            detected = 0

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()
'''def rotateImage(image, angle):
            image_center = tuple(np.array(image.shape[1::-1]) / 2)
            rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
            result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
            return result

        (tl, tr, br, bl) = rect
        angle = np.array((br[0]-tr[0])/(br[1]-tr[1]))
        result = rotateImage(frame, angle)
        cv2.imshow('rotate', frame)'''