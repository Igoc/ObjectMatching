import Utility.Evaluation
import Utility.Loader
import Utility.Preprocessor

import argparse
import cv2
import glob
import os
import pandas   as pd
import sys
import time

def MatchObjectsInTwoImages(leftObjects, leftObjectTypes, rightObjects, rightObjectTypes, threshold=None):
    highestCorrelationScores = list()
    mostSimilarObjectIndexes = list()
    
    for leftObjectIndex in range(len(leftObjects)):
        highestCorrelationScores.append(sys.float_info.min)
        mostSimilarObjectIndexes.append(None)
        
        for rightObjectIndex in range(len(rightObjects)):
            if leftObjectTypes[leftObjectIndex] == rightObjectTypes[rightObjectIndex]:
                leftObject       = leftObjects[leftObjectIndex].ravel()
                rightObject      = rightObjects[rightObjectIndex].ravel()
                correlationScore = cv2.compareHist(leftObject, rightObject, cv2.HISTCMP_CORREL)
                
                if correlationScore > highestCorrelationScores[leftObjectIndex]:
                    highestCorrelationScores[leftObjectIndex] = correlationScore
                    mostSimilarObjectIndexes[leftObjectIndex] = rightObjectIndex
    
    if threshold == None or threshold < -1 or threshold > 1:
        threshold = sum(highestCorrelationScores) / len(highestCorrelationScores)
    
    for leftObjectIndex in range(len(leftObjects)):
        if highestCorrelationScores[leftObjectIndex] < threshold:
            highestCorrelationScores[leftObjectIndex] = None
            mostSimilarObjectIndexes[leftObjectIndex] = None
    
    return highestCorrelationScores, mostSimilarObjectIndexes, threshold

if __name__ == '__main__':
    programStartTime     = time.perf_counter()
    majorTaskElapsedTime = 0.0
    
    argumentParser = argparse.ArgumentParser()
    
    argumentParser.add_argument('--image', type=str, required=True, help='Image directory path')
    argumentParser.add_argument('--marking', type=str, required=True, help='Marking directory path')
    argumentParser.add_argument('--label', type=str, default='', help='Label directory path')
    argumentParser.add_argument('--output', type=str, default='./Output', help='Output directory path')
    argumentParser.add_argument('--objectsize', type=int, default=15, help='Object size to set')
    argumentParser.add_argument('--threshold', type=float, default=0, help='Threshold for correlation score (-1 to 1, otherwise it will be set to average of highest correlation scores)')
    
    arguments = argumentParser.parse_args()
    
    imageDirectoryPath   = arguments.image.replace('\\', '/')
    markingDirectoryPath = arguments.marking.replace('\\', '/')
    labelDirectoryPath   = arguments.label.replace('\\', '/')
    outputDirectoryPath  = arguments.output.replace('\\', '/')
    
    if imageDirectoryPath[-1] != '/':
        imageDirectoryPath += '/'
    
    if markingDirectoryPath[-1] != '/':
        markingDirectoryPath += '/'
    
    if labelDirectoryPath != '' and labelDirectoryPath[-1] != '/':
        labelDirectoryPath += '/'
    
    if outputDirectoryPath[-1] != '/':
        outputDirectoryPath += '/'
    
    if os.path.isdir(outputDirectoryPath) == False:
        os.makedirs(outputDirectoryPath)
    
    objectSize = arguments.objectsize
    threshold  = arguments.threshold
    
    imagePathes   = glob.glob(imageDirectoryPath + '*.bmp') + glob.glob(imageDirectoryPath + '*.jpg') + glob.glob(imageDirectoryPath + '*.jpeg') + glob.glob(imageDirectoryPath + '*.png')
    markingPathes = glob.glob(markingDirectoryPath + '*.txt')
    labelPathes   = None
    
    for imageIndex in range(len(imagePathes)):
        imagePathes[imageIndex] = imagePathes[imageIndex].replace('\\', '/')
    
    if labelDirectoryPath != '':
        labelPathes = glob.glob(labelDirectoryPath + '*.txt')
    
    imageNames               = [imagePathes[imageIndex].split('/')[-1] for imageIndex in range(len(imagePathes) - 1)]
    images, markings, labels = Utility.Loader.LoadDataset(imagePathes, markingPathes, labelPathes)
    
    objectsList     = list()
    objectTypesList = list()
    
    for imageIndex in range(len(images)):
        majorTaskStartTime    = time.process_time()
        objects, objectTypes  = Utility.Preprocessor.CropObjects(images[imageIndex], markings[imageIndex], objectSize)
        majorTaskEndTime      = time.process_time()
        majorTaskElapsedTime += majorTaskEndTime - majorTaskStartTime
        
        objectsList.append(objects)
        objectTypesList.append(objectTypes)
    
    highestCorrelationScoresList = list()
    mostSimilarObjectIndexesList = list()
    thresholdList                = list()
    
    for imageIndex in range(len(images) - 1):
        majorTaskStartTime                                                 = time.process_time()
        highestCorrelationScores, mostSimilarObjectIndexes, usedThreshold  = MatchObjectsInTwoImages(objectsList[imageIndex], objectTypesList[imageIndex], objectsList[imageIndex + 1], objectTypesList[imageIndex + 1], threshold)
        majorTaskEndTime                                                   = time.process_time()
        majorTaskElapsedTime                                              += majorTaskEndTime - majorTaskStartTime
        
        highestCorrelationScoresList.append(highestCorrelationScores)
        mostSimilarObjectIndexesList.append(mostSimilarObjectIndexes)
        thresholdList.append(usedThreshold)
    
    accuracies, totalAccuracy = Utility.Evaluation.EvaluateAccuracyForContinuousImagePairComparison(mostSimilarObjectIndexesList, objectTypesList, labels)
    connectedImages           = Utility.Evaluation.DrawConnectionLineForContinuousImagePairComparison(images, markings, mostSimilarObjectIndexesList)
    programEndTime            = time.perf_counter()
    
    for imageIndex in range(len(connectedImages)):
        cv2.imwrite(outputDirectoryPath + imageNames[imageIndex], connectedImages[imageIndex])
    
    highestCorrelationScoresTable              = pd.DataFrame(highestCorrelationScoresList, index=imageNames)
    highestCorrelationScoresTable.columns.name = 'Object Index'
    highestCorrelationScoresTable.index.name   = 'Image Name'
    
    mostSimilarObjectIndexesTable              = pd.DataFrame(mostSimilarObjectIndexesList, index=imageNames)
    mostSimilarObjectIndexesTable.columns.name = 'Object Index'
    mostSimilarObjectIndexesTable.index.name   = 'Image Name'
    
    thresholdTable            = pd.Series(thresholdList, index=imageNames)
    thresholdTable.index.name = 'Image Name'
    
    accuraciesTable            = pd.Series(accuracies)
    accuraciesTable.index.name = 'Object Index'
    
    print('<Highest Correlation Scores>')
    print(highestCorrelationScoresTable, end='\n\n')
    
    print('<Most Similar Object Indexes>')
    print(mostSimilarObjectIndexesTable, end='\n\n')
    
    print('<Threshold>')
    print(thresholdTable, end='\n\n')
    
    if len(labels) > 0:
        print('<Accuracies>')
        print(accuraciesTable, end='\n\n')
        
        print('<Total Accuracy> {}'.format(totalAccuracy), end='\n\n')
    
    print('<Program Elapsed Time> {}'.format(programEndTime - programStartTime))
    print('<Major Task Elapsed Time> {}'.format(majorTaskElapsedTime))