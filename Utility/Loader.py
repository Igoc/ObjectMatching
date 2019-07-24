import cv2
import numpy as np

def LoadDataset(imagePathes, markingPathes, labelPathes=None):
    images   = list()
    markings = list()
    labels   = list()
    
    if labelPathes != None:
        for imageIndex in range(len(imagePathes)):
            images.append(ReadImageData(imagePathes[imageIndex]))
            markings.append(ReadMarkingData(markingPathes[imageIndex]))
            labels.append(ReadLabelData(labelPathes[imageIndex]))
    else:
        for imageIndex in range(len(imagePathes)):
            images.append(ReadImageData(imagePathes[imageIndex]))
            markings.append(ReadMarkingData(markingPathes[imageIndex]))
    
    return images, markings, labels

def ReadImageData(imagePath):
    return cv2.imread(imagePath, cv2.IMREAD_COLOR).astype(np.float32) / 255.0

def ReadLabelData(labelPath):
    label = list()
    
    with open(labelPath, 'r') as file:
        while True:
            data = file.readline()
            
            if data == None or data == '':
                break
            
            data    = data.split(' ')
            data[0] = int(data[0])
            data[1] = int(data[1])
            
            label.append(data)
    
    return label

def ReadMarkingData(markingPath):
    marking = list()
    
    with open(markingPath, 'r') as file:
        while True:
            data = file.readline()
            
            if data == None or data == '':
                break
            
            data    = data.split(' ')
            data[0] = int(data[0])
            data[1] = float(data[1])
            data[2] = float(data[2])
            data[3] = float(data[3])
            data[4] = float(data[4])
            
            marking.append(data)
    
    return marking