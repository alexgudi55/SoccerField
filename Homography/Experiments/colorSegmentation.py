import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import hsv_to_rgb

#SE transforma a RGB para observar en plt.
field =  cv2.imread("rmVSpsg.jpg",1) #BGR
field = cv2.cvtColor(field,cv2.COLOR_BGR2RGB)


hsvField = cv2.cvtColor(field, cv2.COLOR_RGB2HSV)


darkGreen = (40,85, 50)
lightGreen = (50, 255, 255)


lightGreenSquare = np.full((10, 10, 3), lightGreen, dtype=np.uint8) / 255.0
darkGreenSquare = np.full((10, 10, 3), darkGreen, dtype=np.uint8) / 255.0 ## divided by 255 just for plt to plot them. Simon, sale esto:
#Clipping input data to the valid range for imshow with RGB data ([0..1] for floats or [0..255] for integers)
"""plt.subplot(1, 3, 1)
plt.imshow(hsv_to_rgb(lightGreenSquare))
plt.subplot(1, 3, 2)
plt.imshow(hsv_to_rgb(darkGreenSquare))
plt.subplot(1, 3, 3)
plt.imshow(field)
plt.show()
"""

color = (150, 255, 60)
mask = cv2.inRange(hsvField, darkGreen, lightGreen)
mask_inv = cv2.bitwise_not(mask)
result = cv2.bitwise_and(field, field, mask = mask)
im_out = cv2.line(result, (20,300) , (1000,400), color, 9)
result1 = cv2.bitwise_and(field, field, mask = mask_inv)

kernel = np.ones((5,5),np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
cv2.imshow("mask",mask)
cv2.waitKey(0)

plt.subplot(1, 3, 1)
plt.imshow(mask, cmap="gray")
plt.subplot(1, 3, 2)
plt.imshow(im_out)
plt.subplot(1, 3, 3)
plt.imshow(result1)
plt.show()


im_out = cv2.cvtColor(im_out,cv2.COLOR_RGB2BGR)
result1 = cv2.cvtColor(result1,cv2.COLOR_RGB2BGR)
final = cv2.bitwise_or(im_out,result1,mask = mask)
final = cv2.add(final,result1)
cv2.imshow('res',final)
cv2.imshow('thres',result1)
cv2.waitKey(0)
cv2.destroyAllWindows()