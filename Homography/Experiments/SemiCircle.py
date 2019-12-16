import numpy as np
import cv2

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
	axes = (15, 15)
	angle = 0 ;
	startAngle=0;
	endAngle=180
	color = (0, 0, 255)
	img = cv2.ellipse(img, Point, axes, 
           angle, startAngle, endAngle, color, -1) 
	return img

def main():
	global pointsImage
	global pointsField

	#Read Front View Field Image
	field = openImage("soccer-field-sizes.png")
	#Read the image  
	img = openImage("EnglandGoal.jpg")
	Point =(250,250)

	field = DrawSemiCircle(Point, field)
	cv2.imshow('res',field)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
"""
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
######Off-side########################
	lastPlayer = pointsImage[0]
	pointsImage = np.delete(pointsImage, 0, 0)

	homography, status = cv2.findHomography(pointsField, pointsImage)
	homographyInv, status = cv2.findHomography(pointsImage, pointsField)

	lastPlayer = np.append(lastPlayer, np.array([1]), axis=0)  ##Normalize adding 1 [x,y,1]
	print(lastPlayer)
	lastPlayer = np.transpose(lastPlayer)
	lastPlayerH = np.dot(homographyInv, lastPlayer) ###Dot Product
	print(lastPlayerH)
	s = lastPlayerH[2]    #Extra value
	print(s)
	lastPlayerH = lastPlayerH*(1/s)
	lastPlayerH = np.delete(lastPlayerH, 2)
	print(lastPlayerH)

	##								
	UpPointH = np.array([[lastPlayerH[0],25,1]])  ##25 is the up coordinate 'y' on the  template Field
	DwPointH = np.array([[lastPlayerH[0],358,1]]) ##358 is the down coordinate 'y' on the template Field
	print(UpPointH)
	print(DwPointH)
	##Obtain UpPoint
	UpPointH = np.transpose(UpPointH)
	UpPoint = np.dot(homography, UpPointH) ###Dot Product
	s = UpPoint[2]    #Extra value
	UpPoint = UpPoint*(1/s)
	UpPoint = np.delete(UpPoint, 2)
	print(UpPoint)
	##Obtain Down Point
	DwPointH = np.transpose(DwPointH)
	DwPoint = np.dot(homography, DwPointH) ###Dot Product
	s = DwPoint[2]    #Extra value
	DwPoint = DwPoint*(1/s)
	DwPoint = np.delete(DwPoint, 2)
	print(DwPoint)

	#TrazarLinea
	color = (0, 0, 255)
	imgWithMask = cv2.line(imgWithMask, (int(UpPoint[0]),int(UpPoint[1])), (int(DwPoint[0]),int(DwPoint[1])), color, 2)

	######### Combine Images ##########
	final = cv2.bitwise_or(imgWithMask,imgWithInvMask,mask = mask)
	final = cv2.add(final,imgWithInvMask)
	cv2.imshow('res',final)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
"""
if __name__ == '__main__':
    main()

