import numpy as np
import cv2
import math
import sys

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

def segmentField(img):
    hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	#Define color ranges
    darkGreen = (40,85,50)
    lightGreen = (70, 255, 255)
	#Obtain masks
    mask = cv2.inRange(hsvImg, darkGreen, lightGreen)
    mask_inv = cv2.bitwise_not(mask)
	#Apply masks
    imgWithMask = cv2.bitwise_and(img, img, mask = mask) #Grass
    imgWithInvMask = cv2.bitwise_and(img, img, mask = mask_inv)#Players
    return imgWithMask, imgWithInvMask, mask, mask_inv

def joingImages(imgGrass, imgPlayers, mask):
    img = cv2.bitwise_or(imgGrass,imgPlayers,mask = mask)
    img = cv2.add(img,imgPlayers)
    return img

def addText(img, distance):
    # text 
    text = str(round(distance, 2))+" mts"
    # font 
    font = cv2.FONT_HERSHEY_SIMPLEX 
    # orgin 
    org = img.shape
    org = (int(org[1]*.3), int(org[0]*.9))
    print(org)
    # fontScale 
    fontScale = 1
    # Red color in BGR 
    color = (255, 0, 0) 
    # Line thickness of 2 px 
    thickness = 2
    # Using cv2.putText() method 
    img = cv2.putText(img, text, org, font, fontScale,  
                    color, thickness, cv2.LINE_AA, False)
    return img 

def freeKick(img):
    global pointsImage
    global pointsField
    #Get the coordinates of ball
    ballPoint = pointsImage[0]
    pointsImage = np.delete(pointsImage, 0, 0)
    #Calculate the homographies.
    homography, status = cv2.findHomography(pointsImage, pointsField)
    homographyInv, status = cv2.findHomography(pointsField, pointsImage)
    #Calculo de punto en portería en Img original transformando punto de "Template field" con la homografía.
    goalLineH = (16,216,1) ##Center of the goal line. Normalize adding 1 [x,y,1]
    goalLineH = np.transpose(goalLineH)
    goalLine = np.dot(homographyInv, goalLineH) ###Dot Product
    s = goalLine[2]    #Extra value
    goalLine = goalLine*(1/s)
    goalLine = np.delete(goalLine, 2)
    #Draw line from ball to goal line
    color = (0, 0, 255)
    print(goalLine)
    print(ballPoint)
    img = cv2.line(img, (int(goalLine[0]),int(goalLine[1])), (int(ballPoint[0]),int(ballPoint[1])), color, 2)
    cv2.imshow("LineDrew", img)
    cv2.waitKey(0)
    #Calculate distance
    ballPoint = np.append(ballPoint, np.array([1]), axis=0)
    ballPoint = np.transpose(ballPoint)
    ballPointH = np.dot(homography, ballPoint) 
    s = ballPointH[2]
    ballPointH = ballPointH*(1/s)
    ballPointH = np.delete(ballPointH, 2)
    distance = (((ballPointH[0]-goalLineH[0])**2 + (ballPointH[1]-goalLineH[1])**2)**0.5) / 6
    print(distance)
    #-----------It is still missing the circle----------------------#
    blackField = np.zeros((434,330,3), np.uint8) #656,434
    blackField = cv2.circle(blackField,(int(ballPointH[0]),int(ballPointH[1])),6*9,color,1)
    cv2.imshow("Circle black field", blackField)
    cv2.waitKey(0)
    blackField = cv2.warpPerspective(blackField, homographyInv, (img.shape[1],img.shape[0]))
    cv2.imshow("Circle black field", blackField)
    cv2.waitKey(0)
    blackFieldGray = cv2.cvtColor(blackField, cv2.COLOR_BGR2GRAY)
    ___, mask = cv2.threshold(blackFieldGray,1,255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    cv2.imshow("maskara",mask)
    cv2.waitKey(0)
    img = cv2.bitwise_or(img,blackField,mask = mask_inv)
    img = cv2.add(img,blackField)
    cv2.imshow("AlmostFinal XD", img)
    cv2.waitKey(0)
    
    return img, distance

def offSideLine(img):
    global pointsImage
    global pointsField

    lastPlayer = pointsImage[0]
    pointsImage = np.delete(pointsImage, 0, 0)
    #-Calculate homographies--
    homography, status = cv2.findHomography(pointsImage, pointsField)
    homographyInv, status = cv2.findHomography(pointsField, pointsImage)

    lastPlayer = np.append(lastPlayer, np.array([1]), axis=0)  ##Normalize adding 1 [x,y,1]
    lastPlayer = np.transpose(lastPlayer)
    lastPlayerH = np.dot(homography, lastPlayer) ###Dot Product
    s = lastPlayerH[2]    #Extra value
    lastPlayerH = lastPlayerH*(1/s)
    lastPlayerH = np.delete(lastPlayerH, 2)
    ##								
    UpPointH = np.array([[lastPlayerH[0],16,1]])  ##16 is the up coordinate 'y' on the  template Field
    DwPointH = np.array([[lastPlayerH[0],417,1]]) ##417 is the down coordinate 'y' on the template Field
    ##Obtain UpPoint
    UpPointH = np.transpose(UpPointH)
    UpPoint = np.dot(homographyInv, UpPointH) ###Dot Product
    s = UpPoint[2]    #Extra value
    UpPoint = UpPoint*(1/s)
    UpPoint = np.delete(UpPoint, 2)
    ##Obtain Down Point
    DwPointH = np.transpose(DwPointH)
    DwPoint = np.dot(homographyInv, DwPointH) ###Dot Product
    s = DwPoint[2]    #Extra value
    DwPoint = DwPoint*(1/s)
    DwPoint = np.delete(DwPoint, 2)
    #TrazarLinea
    color = (0, 0, 255)
    img = cv2.line(img, (int(UpPoint[0]),int(UpPoint[1])), (int(DwPoint[0]),int(DwPoint[1])), color, 2)
    cv2.imshow("OffsideLine", img)
    cv2.waitKey(0)
    return img

"""
To run this script:
    python soccerHomography.py freekick EnglandGoal.jpg soccer-field-sizes.png
"""
def main():
    global pointsImage
    global pointsField
    DATASET_PATH = "images/"
    if(len(sys.argv) < 4):
        print("Error: Expected 4 arguments. To run this code: python soccerHomography.py action imageName fieldName")
        return
    fieldPath = sys.argv[3]
    imagePath = sys.argv[2]
    action = sys.argv[1]
	#Read Front View Field Image
    field = openImage(DATASET_PATH+fieldPath)
    #Read the image  
    img = openImage(DATASET_PATH+imagePath)
    #Select feducial Points.
    SelectFedPoints(field, img)
    #Segment grass and players
    imgGrass, imgPlayers, mask, __ = segmentField(img)
    if(action == "freekick"):
        imgGrass, distance = freeKick(imgGrass)
        finalImg = joingImages(imgGrass, imgPlayers,mask)
        finalImg = addText(finalImg,distance)
    else:
        imgGrass = offSideLine(imgGrass)
        finalImg = joingImages(imgGrass, imgPlayers,mask)
    cv2.imshow("Final image", finalImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()