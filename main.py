
import re
import cv2
import numpy as np
import pytesseract
from pip._internal.cli.cmdoptions import src
import random
import colorsys
from tensorflow import tf
from core.config import cfg

def recognize_plate(img, coords):
   xmin, ymin, xmax, ymax = coords
   box = img[int(ymin)-5: int(ymax)+5, int(xmin)-5: int(xmax)+5]
   gray = cv2.cvtColor(box, cv2.COLOR_BGR2GRAY)
   gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
   blur = cv2.GaussianBlur(gray, (7, 7), cv2.BORDER_DEFAULT)
   cv2.imshow("gray", blur)
   ret, thresh1 = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
   rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
   dilation = cv2.dilate(thresh1, rect_kern, iterations=1)
   cv2.imshow("dilation", dilation)
   contours, hierarechy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   sorted_contours = sorted(contours, key=lambda ctr: cv2.boundingRect[0])
   image2 = gray.copy(0)
   plate_num: " "
   for cnt in sorted_contours:
