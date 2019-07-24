import cv2

def CropObjects(image, marking, objectSize):
    objects     = list()
    objectTypes = list()
    
    imageHeight, imageWidth = image.shape[:2]
    
    for objectIndex in range(len(marking)):
        objectWidth    = int(marking[objectIndex][3] * imageWidth + 0.5)
        objectHeight   = int(marking[objectIndex][4] * imageHeight + 0.5)
        objectTopLeftX = int(marking[objectIndex][1] * imageWidth - objectWidth / 2.0 + 0.5)
        objectTopLeftY = int(marking[objectIndex][2] * imageHeight - objectHeight / 2.0 + 0.5)
        
        objects.append(image[objectTopLeftY : objectTopLeftY + objectHeight, objectTopLeftX : objectTopLeftX + objectWidth])
        objectTypes.append(marking[objectIndex][0])
        
        objects[objectIndex] = cv2.resize(objects[objectIndex], (objectSize, objectSize), interpolation=cv2.INTER_LINEAR)
    
    return objects, objectTypes