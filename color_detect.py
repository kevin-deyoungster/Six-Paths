import cv2
import imutils
import numpy as np

RED_LOWER = [140,150,0]
RED_UPPER = [170,255,255]
BLUE_LOWER = [100,150,0]
BLUE_UPPER = [140,255,255] 

def detect_color(image_path, lower_color, upper_color):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array(lower_color), np.array(upper_color))
    kernel = np.ones((9,9),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    edged = cv2.Canny(mask, 75, 200)
    cv2.imshow('masked', edged)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    cv2.drawContours(image, [cnts[0]], -1, (0, 255, 0), 2)
    cv2.imshow(image_path, image)

    # res = cv2.bitwise_and(image,image,mask=mask)
    # cv2.imshow('frame', image)
    # cv2.imshow('res', res)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def convert_to_hsv(r,g,b):
    return cv2.cvtColor(np.uint8([[[b,g,r]]]),cv2.COLOR_BGR2HSV)

def convert_hsv_to_rgb(hsv):
    return cv2.cvtColor(np.uint8([[hsv]]),cv2.COLOR_HSV2RGB)


from pathlib import Path
pathlist = Path("images").glob('**/*.JPG')
for path in pathlist:
    detect_color(str(path), BLUE_LOWER,BLUE_UPPER)
    detect_color(str(path), RED_LOWER,RED_UPPER)