import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("EnglandGoal.jpg",1)

hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)	
lower_green = np.array([40,40, 40])
upper_green = np.array([70, 255, 255])
#blue range
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

#Red range
lower_red = np.array([0,31,255])
upper_red = np.array([176,255,255])

#white range
lower_white = np.array([0,0,0])
upper_white = np.array([0,0,255])

#Define a mask ranging from lower to uppper
mask = cv2.inRange(hsv, lower_green, upper_green)
#Do masking
res = cv2.bitwise_and(img, img, mask=mask)

res_bgr = cv2.cvtColor(res,cv2.COLOR_HSV2BGR)
res_gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)

#Defining a kernel to do morphological operation in threshold image to 
#get better output.
kernel = np.ones((13,13),np.uint8)
thresh = cv2.threshold(res_gray,127,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

res = cv2.bitwise_and(img, img, mask=thresh)

cv2.imshow("Mask",res)
cv2.waitKey(0)