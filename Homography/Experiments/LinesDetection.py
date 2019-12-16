import cv2
import numpy as np

img = cv2.imread("EnglandGoal.jpg")

hsvField = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
darkGreen = (40,120, 50)
lightGreen = (70, 255, 255)
mask = cv2.inRange(hsvField, darkGreen, lightGreen)
mask_inv = cv2.bitwise_not(mask)

kernel =  np.ones((2,2),np.uint8)
closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

edges = cv2.Canny(closing,50,150,apertureSize = 7)
cv2.imshow('houghles',closing)
cv2.imshow('houghline',edges)
cv2.waitKey(0)


lines = cv2.HoughLines(edges,1/2,np.pi/360,70)

for line in lines:
    for rho,theta in line:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imshow('houghlines',img)
cv2.waitKey(0)
