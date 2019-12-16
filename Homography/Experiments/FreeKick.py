import numpy as np
import cv2
import math

pointsImage = np.array([[1,1]]) 
pointsField = np.array([[1,1]]) 

def openImage(filename):
    try:
    	img = cv2.imread(filename,1)
    except:
        print("Error reading image: ", filename)
        return None
    return img

def SelectFedPoints(field, img):

	global pointsImage
	global pointsField

	cv2.namedWindow('ImagePoints')
	cv2.setMouseCallback('ImagePoints',getPointsImg)
	while(True):
		cv2.imshow('ImagePoints',img)
		k = cv2.waitKey(20) & 0xFF
		if k == 27:
			break
	pointsImage = np.delete(pointsImage, 0, 0)		    
	

	cv2.namedWindow('FieldPoints')
	cv2.setMouseCallback('FieldPoints',getPointsField)
	while(True):
		cv2.imshow('FieldPoints',field)
		k = cv2.waitKey(20) & 0xFF
		if k == 27:
			break
	pointsField = np.delete(pointsField, 0, 0)		    
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def getPointsImg(event,x,y,flags,param):
    global pointsImage
    if event == cv2.EVENT_LBUTTONUP:
        pointsImage = np.append(pointsImage,[[x,y]], axis = 0)


def getPointsField(event,x,y,flags,param):
    global pointsField
    if event == cv2.EVENT_LBUTTONUP:
        pointsField = np.append(pointsField,[[x,y]], axis = 0)

def DrawSemiCircle(Point, img):
	end_point = (34,191)
	punto = (Point[0],Point[1]) 
	axes = (15, 15)
	angle = 0 ;
	startAngle=0;
	endAngle=180
	color = (0, 0, 255)
	img = cv2.ellipse(img, punto, axes, 
           angle, startAngle, endAngle, color, -1) 
	return img

def main():
	global pointsImage
	global pointsField

	#Read Front View Field Image
	field = openImage("soccer-field-sizes.png")
	#Read the image  
	img = openImage("EnglandGoal.jpg")

	#Select feducial Points.
	SelectFedPoints(field, img)

######IMAGE SEGMENTATION###########
	hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	#Define color ranges
	darkGreen = (40,85, 50)
	lightGreen = (60, 255, 255)
	#Obtain masks
	mask = cv2.inRange(hsvImg, darkGreen, lightGreen)
	mask_inv = cv2.bitwise_not(mask)
	#Apply masks
	#HISTOGRAM BACKPROJECTION CHECAR
	imgWithMask = cv2.bitwise_and(img, img, mask = mask)
	imgWithInvMask = cv2.bitwise_and(img, img, mask = mask_inv)
	cv2.imshow("Maskara", mask_inv)
	cv2.imshow("Mask",imgWithMask)
	cv2.imshow("Mask Inv",imgWithInvMask)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

##########HOMOGRAPHY#############
	#Free kick#
	ballPoint = pointsImage[0]
	pointsImage = np.delete(pointsImage, 0, 0)

	homography, status = cv2.findHomography(pointsImage, pointsField)
	homographyInv, status = cv2.findHomography(pointsField, pointsImage)
	#Calculo de punto en portería en Img original transformando punto de "Template field" con la homografía.
	end_point = (34,191) 
	end_point = np.append(end_point, np.array([1]), axis=0)  ##Normalize adding 1 [x,y,1]
	end_point = np.transpose(end_point)
	newPoint = np.dot(homographyInv, end_point) ###Dot Product
	s = newPoint[2]    #Extra value
	newPoint = newPoint*(1/s)
	newPoint = np.delete(newPoint, 2)
	#Calculate distance
	print("homography Inv:    ",homography)
	TballPoint = np.append(ballPoint, np.array([1]), axis=0)
	print("Adding 1:  ", TballPoint)
	TballPoint = np.transpose(TballPoint)
	print(TballPoint)
	TballPoint = np.dot(homography, TballPoint) 
	s = TballPoint[2]
	TballPoint = TballPoint*(1/s)
	TballPoint = np.delete(TballPoint, 2)
	print(TballPoint)
	distance = (((TballPoint[0]-end_point[0])**2 + (TballPoint[1]-end_point[1])**2)**0.5) / 3.63
	print(distance)
	#Trazar linea.
	color = (0, 0, 255)
	imgWithMask = cv2.line(imgWithMask, (int(newPoint[0]),int(newPoint[1])), (int(ballPoint[0]),int(ballPoint[1])), color, 2)
	#Dibujar Semicirculo
	imgWithMask = DrawSemiCircle(ballPoint, imgWithMask)
######### Combine Images ##########
	final = cv2.bitwise_or(imgWithMask,imgWithInvMask,mask = mask)
	final = cv2.add(final,imgWithInvMask)
	cv2.imshow('res',final)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	

if __name__ == '__main__':
    main()

