import cv2
import numpy as np
import sys

def DrawConnectionLineForContinuousImagePairComparison(images, markings, mostSimilarObjectIndexesList):
    outputImages = list()
    
    for imageIndex in range(len(images) - 1):
        outputImage             = (cv2.hconcat([images[imageIndex], images[imageIndex + 1]]) * 255.0).astype(np.uint8)
        imageHeight, imageWidth = images[imageIndex].shape[:2]
        
        for rightObjectIndex in range(len(markings[imageIndex + 1])):
            rightObjectWidth    = int(markings[imageIndex + 1][rightObjectIndex][3] * imageWidth + 0.5)
            rightObjectHeight   = int(markings[imageIndex + 1][rightObjectIndex][4] * imageHeight + 0.5)
            rightObjectTopLeftX = int(markings[imageIndex + 1][rightObjectIndex][1] * imageWidth - rightObjectWidth / 2.0 + 0.5)
            rightObjectTopLeftY = int(markings[imageIndex + 1][rightObjectIndex][2] * imageHeight - rightObjectHeight / 2.0 + 0.5)
            
            outputImage = cv2.rectangle(outputImage, (rightObjectTopLeftX + imageWidth, rightObjectTopLeftY), (rightObjectTopLeftX + rightObjectWidth + imageWidth, rightObjectTopLeftY + rightObjectHeight), (255, 0, 0))
        
        for leftObjectIndex in range(len(markings[imageIndex])):
            leftObjectWidth    = int(markings[imageIndex][leftObjectIndex][3] * imageWidth + 0.5)
            leftObjectHeight   = int(markings[imageIndex][leftObjectIndex][4] * imageHeight + 0.5)
            leftObjectCenterX  = int(markings[imageIndex][leftObjectIndex][1] * imageWidth + 0.5)
            leftObjectCenterY  = int(markings[imageIndex][leftObjectIndex][2] * imageHeight + 0.5)
            leftObjectTopLeftX = int(leftObjectCenterX - leftObjectWidth / 2.0 + 0.5)
            leftObjectTopLeftY = int(leftObjectCenterY - leftObjectHeight / 2.0 + 0.5)
            
            outputImage = cv2.rectangle(outputImage, (leftObjectTopLeftX, leftObjectTopLeftY), (leftObjectTopLeftX + leftObjectWidth, leftObjectTopLeftY + leftObjectHeight), (0, 0, 255))
            
            if mostSimilarObjectIndexesList[imageIndex][leftObjectIndex] != None:
                matchedObjectCenterX = int(markings[imageIndex + 1][mostSimilarObjectIndexesList[imageIndex][leftObjectIndex]][1] * imageWidth + 0.5)
                matchedObjectCenterY = int(markings[imageIndex + 1][mostSimilarObjectIndexesList[imageIndex][leftObjectIndex]][2] * imageHeight + 0.5)
                
                outputImage = cv2.line(outputImage, (leftObjectCenterX, leftObjectCenterY), (matchedObjectCenterX + imageWidth, matchedObjectCenterY), (0, 255, 0))
        
        outputImages.append(outputImage)
    
    return outputImages

def EvaluateAccuracyForContinuousImagePairComparison(mostSimilarObjectIndexesList, objectTypesList, labels):
    objectTypeNumber = -sys.maxsize - 1
    
    for objectTypes in objectTypesList:
        highestObjectTypeIndex = max(objectTypes)
        
        if highestObjectTypeIndex > objectTypeNumber:
            objectTypeNumber = highestObjectTypeIndex + 1
    
    objectCounts     = [0 for objectTypeIndex in range(objectTypeNumber)]
    totalObjectCount = 0
    
    accuracies    = [0.0 for objectTypeIndex in range(objectTypeNumber)]
    totalAccuracy = 0.0
    
    for imageIndex in range(len(labels) - 1):
        for leftObjectIndex in range(len(labels[imageIndex])):
            mostSimilarObjectIndex                                      = mostSimilarObjectIndexesList[imageIndex][leftObjectIndex]
            objectCounts[objectTypesList[imageIndex][leftObjectIndex]] += 1
            totalObjectCount                                           += 1
            
            if mostSimilarObjectIndex != None and labels[imageIndex][leftObjectIndex][1] == labels[imageIndex + 1][mostSimilarObjectIndex][1]:
                accuracies[objectTypesList[imageIndex][leftObjectIndex]] += 1
                totalAccuracy                                            += 1
            elif mostSimilarObjectIndex == None:
                sameObjectExistence = False
                
                for rightObjectIndex in range(len(labels[imageIndex + 1])):
                    if labels[imageIndex][leftObjectIndex][0] == labels[imageIndex + 1][rightObjectIndex][0] and labels[imageIndex][leftObjectIndex][1] == labels[imageIndex + 1][rightObjectIndex][1]:
                        sameObjectExistence = True
                        break
                
                if sameObjectExistence == False:
                    accuracies[objectTypesList[imageIndex][leftObjectIndex]] += 1
                    totalAccuracy                                            += 1
    
    for objectTypeIndex in range(objectTypeNumber):
        if objectCounts[objectTypeIndex] != 0:
            accuracies[objectTypeIndex] /= objectCounts[objectTypeIndex]
    totalAccuracy /= totalObjectCount
    
    return accuracies, totalAccuracy