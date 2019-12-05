import cv2
import numpy as np


Points1 = np.array([[1,1]]) 
Points2 = np.array([[1,1]]) 
c = 0
# mouse callback function
def getPoints(event,x,y,flags,param):
    global Points1, c
    if event == cv2.EVENT_LBUTTONUP:
        Points1 = np.append(Points1,[[x,y]], axis = 0)
        c+=1
def getPoints1(event,x,y,flags,param):
    global Points2, c
    if event == cv2.EVENT_LBUTTONUP:
        Points2 = np.append(Points2,[[x,y]], axis = 0)
        c+=1


img = cv2.imread("rmVSpsg.jpg")
cv2.namedWindow('image')
cv2.setMouseCallback('image',getPoints)

while(c < 5):
    cv2.imshow('image',img)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
Points1 = np.delete(Points1, 0, 0)


img2 = cv2.imread("soccer-field-sizes.png")
cv2.namedWindow('image')
cv2.setMouseCallback('image',getPoints1)

while(c < 9):
    cv2.imshow('image',img2)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
Points2 = np.delete(Points2, 0, 0)
distance = Points1[0]
print (distance)

Points1 = np.delete(Points1, 0, 0)

# Calculate Homography
h, status = cv2.findHomography(Points2, Points1)


# Warp source image to destination based on homography
im_out = cv2.warpPerspective(img2, h, (img.shape[1],img.shape[0]))
#transformed = cv2.perspectiveTransform(points, homography)

#Calculo de punto en portería en Img original transformando punto de "Template field" con la homografía.
end_point = (34,191) 
end_point = np.append(end_point, np.array([1]), axis=0) 
end_point = np.transpose(end_point)
newPoint = np.dot(h, end_point)
s = newPoint[2]
newPoint = newPoint*(1/s)
newPoint = np.delete(newPoint, 2)
print(newPoint)

##YA traza linea a la meta desde tiro libre.
color = (0, 0, 255)
imgLinea = img
imgLinea = cv2.line(imgLinea, (int(newPoint[0]),int(newPoint[1])), (int(distance[0]),int(distance[1])), color, 2)


#homography_inverse = np.linalg.inv(h)
#im_out = cv2.warpPerspective(im_out, homography_inverse, (img.shape[1],img.shape[0]))

# Display images
cv2.imshow("Source Image", img)
cv2.imshow("Destination Image", img2)
cv2.imshow("Warped Source Image", imgLinea)

cv2.waitKey(0)

