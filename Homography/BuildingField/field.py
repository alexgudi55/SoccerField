import cv2
import numpy as np

img = np.full((435,657,3),255,np.uint8)
img = cv2.rectangle(img,(16,16),(639,417),(0,0,255),1)
areaGrandeX = 98
areaGrandeY = 241
areaChicaX = 32
areaChicaY = 109
porteriaY = 43
porteriaX = 11
img = cv2.rectangle(img,(16,92),(areaGrandeX+16,areaGrandeY+92),(0,0,255),1)
img = cv2.rectangle(img,(639 - areaGrandeX,92),(639,82 + areaGrandeY),(0,0,255),1)

img = cv2.rectangle(img,(16,158),(areaChicaX+16,areaChicaY+158),(0,0,255),1)
img = cv2.rectangle(img,(639 - areaChicaX,158),(639,158 + areaChicaY),(0,0,255),1)


img = cv2.rectangle(img,(16,191),(porteriaX+16,porteriaY+191),(0,0,255),1)
img = cv2.rectangle(img,(639 - porteriaX,191),(639,191 + porteriaY),(0,0,255),1)




cv2.imshow("lala",img)
cv2.waitKey(0)

cv2.imwrite("field.jpg",img)