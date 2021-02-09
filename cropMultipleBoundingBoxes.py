"""
Project: Crops multiple bounding boxes of exuvia, instars and adults and creates new images to each object anottated.
Author: Rubens de Castro Pereira
Advisor: Dibio Leandro Borges
Date: 14/01/2021
Version: 1.0.0
"""

#
# Create all bounding boxes files in the Yolo format where each annotated object produces until 9(nine) new cropped images
# with the object positioned in different positions.

# Importing needed libraries

import os
# from re import _expand

import cv2

from Entity.BoundingBox import BoundingBox
from Entity.Image import Image
from Entity.Pixel import Pixel
from Entity.GroundTruthData import GroundTruthData
from Entity.DetectedObject import DetectedObject

# ###########################################
# Constants
# ###########################################
LINE_FEED = '\n'
# ANNOTATED_BOUNDING_BOXES_DATABASE_PATH = 'C:/Users/Rubens/Google Drive (rubens.castro@ufg.br)/DoctoralProjects/ImageDatabaseForYolo/5.1 White Fly-Original images for training-validation-test/train-valid/'
# CROPPED_BOUNDING_BOXES_DATABASE_PATH = 'C:/Temp/White Fly-Cropped Bounding Boxes Images/'

# ANNOTATED_BOUNDING_BOXES_DATABASE_PATH = 'C:/Users/Rubens/Google Drive (rubens.castro@ufg.br)/DoctoralProjects/ImageDatabaseForYolo/5.1 White Fly-Original images for training-validation-test/test/'
ANNOTATED_BOUNDING_BOXES_DATABASE_PATH = 'E:/desenvolvimento/projetos/DoctoralProjects/Images-Input-Output/Input - White Fly - Original Images/'
CROPPED_BOUNDING_BOXES_DATABASE_PATH = 'E:/desenvolvimento/projetos/DoctoralProjects/Images-Input-Output/Output - White Fly - Cropped Bounding Boxes Images by Classes/'


# CROPPED_BOUNDING_BOXES_DATABASE_PATH = 'C:/Temp/White Fly-Cropped Bounding Boxes Images - test/'


# ###########################################
# Application Methods
# ###########################################


# crops the bounding box image
def cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage,
                    croppedImagesPath, imageName, className, idBoundingBox, objectPosition):
    # initializing the variables and objects
    # croppedBoundingBoxImage = None
    # objectPosition = 'center'

    # # defining rectangle to crop the original image
    # linP1 = annotatedBoundingBox.linPoint1
    # colP1 = annotatedBoundingBox.colPoint1
    # linP2 = annotatedBoundingBox.linPoint2
    # colP2 = annotatedBoundingBox.colPoint2
    #
    # # adjusting cropped image dimensions
    # heightBoundingBox = linP2 - linP1
    # widthBoundingBox = colP2 - colP1
    #
    # heightDifference = sizeSquareImage - heightBoundingBox
    # widthDifference = sizeSquareImage - widthBoundingBox
    # halfOfHeightDifference = int(heightDifference / 2.0)
    # halfOfWidthDifference = int(widthDifference / 2.0)
    # linP1 = linP1 - halfOfHeightDifference
    # colP1 = colP1 - halfOfWidthDifference
    # linP2 = linP2 + halfOfHeightDifference
    # colP2 = colP2 + halfOfWidthDifference
    #
    # if (linP2 - linP1) % 32 != 0:
    #     linP2 += 1
    # if (colP2 - colP1) % 32 != 0:
    #     colP2 += 1

    # calculating the new coordinates of cropped image
    if objectPosition == 'center':
        linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInCenter(annotatedBoundingBox)
    elif objectPosition == 'north':
        linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInNorth(annotatedBoundingBox)
    elif objectPosition == 'south':
        linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInSouth(annotatedBoundingBox)
    elif objectPosition == 'east':
        linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInEast(annotatedBoundingBox)
    elif objectPosition == 'west':
        linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInWest(annotatedBoundingBox)
    elif objectPosition == 'northeast':
        linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInNortheast(annotatedBoundingBox)
    elif objectPosition == 'northwest':
        linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInNorthwest(annotatedBoundingBox)
    elif objectPosition == 'southeast':
        linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInSoutheast(annotatedBoundingBox)
    elif objectPosition == 'southwest':
        linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInSouthwest(annotatedBoundingBox)

    # evaluating if is possible create the cropped bounding box
    if (linP1 < 0 or colP1 < 0 or linP2 < 0 or colP2 < 0):
        return False

        # cropping and saving bounding box in new image
    croppedBoundingBoxImage = annotatedImage[linP1:linP2, colP1:colP2]
    croppedImageWidth = linP2 - linP1
    croppedImageHeight = colP2 - colP1

    # setting the full path and image name
    croppedImagePathAndImageName = getCroppedBoundingBoxImageName(croppedImagesPath, imageName,
                                                                  className, idBoundingBox, objectPosition)

    # saving the cropped image
    saveCroppedBoundingBoxImage(croppedImagePathAndImageName, croppedBoundingBoxImage)

    # saving cropped annotation file
    saveCroppedBoundingBoxAnnotationFile(croppedImageWidth, croppedImageHeight, croppedImagePathAndImageName,
                                         annotatedBoundingBox, linP1, colP1, linP2, colP2)

    return True


# calculates the new coordinates of the cropped image of bounding box
def calculateNewCoordinatesOfBoundingBoxInCenter(annotatedBoundingBox):
    # defining rectangle to crop the original image
    linP1 = annotatedBoundingBox.linPoint1
    colP1 = annotatedBoundingBox.colPoint1
    linP2 = annotatedBoundingBox.linPoint2
    colP2 = annotatedBoundingBox.colPoint2

    # calculating the dimensions of cropped image
    heightBoundingBox = linP2 - linP1
    widthBoundingBox = colP2 - colP1

    # calculating the new position of bounding box according the position
    heightDifference = sizeSquareImage - heightBoundingBox
    widthDifference = sizeSquareImage - widthBoundingBox
    halfOfHeightDifference = int(heightDifference / 2.0)
    halfOfWidthDifference = int(widthDifference / 2.0)

    # setting the new coordinates
    linP1 = linP1 - halfOfHeightDifference
    colP1 = colP1 - halfOfWidthDifference
    linP2 = linP2 + halfOfHeightDifference
    colP2 = colP2 + halfOfWidthDifference

    # fine adjusting in the positions
    if (linP2 - linP1) % 32 != 0:
        linP2 += 1
    if (colP2 - colP1) % 32 != 0:
        colP2 += 1

    return linP1, colP1, linP2, colP2


# calculates the new coordinates of the cropped image of bounding box
def calculateNewCoordinatesOfBoundingBoxInNorth(annotatedBoundingBox):
    # defining rectangle to crop the original image
    linP1 = annotatedBoundingBox.linPoint1
    colP1 = annotatedBoundingBox.colPoint1
    linP2 = annotatedBoundingBox.linPoint2
    colP2 = annotatedBoundingBox.colPoint2

    # calculating the dimensions of cropped image
    heightBoundingBox = linP2 - linP1
    widthBoundingBox = colP2 - colP1

    # calculating the new position of bounding box according the position
    heightDifference = sizeSquareImage - heightBoundingBox
    widthDifference = sizeSquareImage - widthBoundingBox
    halfOfHeightDifference = int(heightDifference / 2.0)
    halfOfWidthDifference = int(widthDifference / 2.0)

    # setting the new coordinates
    linP1 = linP1
    colP1 = colP1 - halfOfWidthDifference
    linP2 = linP1 + sizeSquareImage
    colP2 = colP2 + halfOfWidthDifference

    # fine adjusting in the positions
    if (linP2 - linP1) % 32 != 0:
        linP2 += 1
    if (colP2 - colP1) % 32 != 0:
        colP2 += 1

    return linP1, colP1, linP2, colP2


# calculates the new coordinates of the cropped image of bounding box
def calculateNewCoordinatesOfBoundingBoxInSouth(annotatedBoundingBox):
    # defining rectangle to crop the original image
    linP1 = annotatedBoundingBox.linPoint1
    colP1 = annotatedBoundingBox.colPoint1
    linP2 = annotatedBoundingBox.linPoint2
    colP2 = annotatedBoundingBox.colPoint2

    # calculating the dimensions of cropped image
    heightBoundingBox = linP2 - linP1
    widthBoundingBox = colP2 - colP1

    # calculating the new position of bounding box according the position
    heightDifference = sizeSquareImage - heightBoundingBox
    widthDifference = sizeSquareImage - widthBoundingBox
    halfOfHeightDifference = int(heightDifference / 2.0)
    halfOfWidthDifference = int(widthDifference / 2.0)

    # setting the new coordinates
    linP1 = linP1 - sizeSquareImage + heightBoundingBox
    colP1 = colP1 - halfOfWidthDifference
    linP2 = linP2
    colP2 = colP2 + halfOfWidthDifference

    # fine adjusting in the positions
    if (linP2 - linP1) % 32 != 0:
        linP2 += 1
    if (colP2 - colP1) % 32 != 0:
        colP2 += 1

    return linP1, colP1, linP2, colP2


# calculates the new coordinates of the cropped image of bounding box
def calculateNewCoordinatesOfBoundingBoxInEast(annotatedBoundingBox):
    # defining rectangle to crop the original image
    linP1 = annotatedBoundingBox.linPoint1
    colP1 = annotatedBoundingBox.colPoint1
    linP2 = annotatedBoundingBox.linPoint2
    colP2 = annotatedBoundingBox.colPoint2

    # calculating the dimensions of cropped image
    heightBoundingBox = linP2 - linP1
    widthBoundingBox = colP2 - colP1

    # calculating the new position of bounding box according the position
    heightDifference = sizeSquareImage - heightBoundingBox
    widthDifference = sizeSquareImage - widthBoundingBox
    halfOfHeightDifference = int(heightDifference / 2.0)
    halfOfWidthDifference = int(widthDifference / 2.0)

    # setting the new coordinates
    linP1 = linP1 - halfOfHeightDifference
    colP1 = colP2 - sizeSquareImage
    linP2 = linP2 + halfOfHeightDifference
    colP2 = colP2

    # fine adjusting in the positions
    if (linP2 - linP1) % 32 != 0:
        linP2 += 1
    if (colP2 - colP1) % 32 != 0:
        colP2 += 1

    return linP1, colP1, linP2, colP2


# calculates the new coordinates of the cropped image of bounding box
def calculateNewCoordinatesOfBoundingBoxInWest(annotatedBoundingBox):
    # defining rectangle to crop the original image
    linP1 = annotatedBoundingBox.linPoint1
    colP1 = annotatedBoundingBox.colPoint1
    linP2 = annotatedBoundingBox.linPoint2
    colP2 = annotatedBoundingBox.colPoint2

    # calculating the dimensions of cropped image
    heightBoundingBox = linP2 - linP1
    widthBoundingBox = colP2 - colP1

    # calculating the new position of bounding box according the position
    heightDifference = sizeSquareImage - heightBoundingBox
    widthDifference = sizeSquareImage - widthBoundingBox
    halfOfHeightDifference = int(heightDifference / 2.0)
    halfOfWidthDifference = int(widthDifference / 2.0)

    # setting the new coordinates
    linP1 = linP1 - halfOfHeightDifference
    colP1 = colP1
    linP2 = linP2 + halfOfHeightDifference
    colP2 = colP1 + sizeSquareImage

    # fine adjusting in the positions
    if (linP2 - linP1) % 32 != 0:
        linP2 += 1
    if (colP2 - colP1) % 32 != 0:
        colP2 += 1

    return linP1, colP1, linP2, colP2


# calculates the new coordinates of the cropped image of bounding box
def calculateNewCoordinatesOfBoundingBoxInNortheast(annotatedBoundingBox):
    # defining rectangle to crop the original image
    linP1 = annotatedBoundingBox.linPoint1
    colP1 = annotatedBoundingBox.colPoint1
    linP2 = annotatedBoundingBox.linPoint2
    colP2 = annotatedBoundingBox.colPoint2

    # calculating the dimensions of cropped image
    heightBoundingBox = linP2 - linP1
    widthBoundingBox = colP2 - colP1

    # calculating the new position of bounding box according the position
    heightDifference = sizeSquareImage - heightBoundingBox
    widthDifference = sizeSquareImage - widthBoundingBox
    halfOfHeightDifference = int(heightDifference / 2.0)
    halfOfWidthDifference = int(widthDifference / 2.0)

    # setting the new coordinates
    linP1 = linP1
    colP1 = colP1 - sizeSquareImage + widthBoundingBox
    linP2 = linP2 + sizeSquareImage - heightBoundingBox
    colP2 = colP2

    # fine adjusting in the positions
    if (linP2 - linP1) % 32 != 0:
        linP2 += 1
    if (colP2 - colP1) % 32 != 0:
        colP2 += 1

    return linP1, colP1, linP2, colP2


# calculates the new coordinates of the cropped image of bounding box
def calculateNewCoordinatesOfBoundingBoxInNorthwest(annotatedBoundingBox):
    # defining rectangle to crop the original image
    linP1 = annotatedBoundingBox.linPoint1
    colP1 = annotatedBoundingBox.colPoint1
    linP2 = annotatedBoundingBox.linPoint2
    colP2 = annotatedBoundingBox.colPoint2

    # calculating the dimensions of cropped image
    heightBoundingBox = linP2 - linP1
    widthBoundingBox = colP2 - colP1

    # calculating the new position of bounding box according the position
    heightDifference = sizeSquareImage - heightBoundingBox
    widthDifference = sizeSquareImage - widthBoundingBox
    halfOfHeightDifference = int(heightDifference / 2.0)
    halfOfWidthDifference = int(widthDifference / 2.0)

    # setting the new coordinates
    linP1 = linP1
    colP1 = colP1
    linP2 = linP2 + sizeSquareImage - heightBoundingBox
    colP2 = colP2 + sizeSquareImage - widthBoundingBox

    # fine adjusting in the positions
    if (linP2 - linP1) % 32 != 0:
        linP2 += 1
    if (colP2 - colP1) % 32 != 0:
        colP2 += 1

    return linP1, colP1, linP2, colP2


# calculates the new coordinates of the cropped image of bounding box
def calculateNewCoordinatesOfBoundingBoxInSoutheast(annotatedBoundingBox):
    # defining rectangle to crop the original image
    linP1 = annotatedBoundingBox.linPoint1
    colP1 = annotatedBoundingBox.colPoint1
    linP2 = annotatedBoundingBox.linPoint2
    colP2 = annotatedBoundingBox.colPoint2

    # calculating the dimensions of cropped image
    heightBoundingBox = linP2 - linP1
    widthBoundingBox = colP2 - colP1

    # calculating the new position of bounding box according the position
    heightDifference = sizeSquareImage - heightBoundingBox
    widthDifference = sizeSquareImage - widthBoundingBox
    halfOfHeightDifference = int(heightDifference / 2.0)
    halfOfWidthDifference = int(widthDifference / 2.0)

    # setting the new coordinates
    linP1 = linP1 - sizeSquareImage + heightBoundingBox
    colP1 = colP1 - sizeSquareImage + widthBoundingBox
    linP2 = linP2
    colP2 = colP2

    # fine adjusting in the positions
    if (linP2 - linP1) % 32 != 0:
        linP2 += 1
    if (colP2 - colP1) % 32 != 0:
        colP2 += 1

    return linP1, colP1, linP2, colP2


# calculates the new coordinates of the cropped image of bounding box
def calculateNewCoordinatesOfBoundingBoxInSouthwest(annotatedBoundingBox):
    # defining rectangle to crop the original image
    linP1 = annotatedBoundingBox.linPoint1
    colP1 = annotatedBoundingBox.colPoint1
    linP2 = annotatedBoundingBox.linPoint2
    colP2 = annotatedBoundingBox.colPoint2

    # calculating the dimensions of cropped image
    heightBoundingBox = linP2 - linP1
    widthBoundingBox = colP2 - colP1

    # calculating the new position of bounding box according the position
    heightDifference = sizeSquareImage - heightBoundingBox
    widthDifference = sizeSquareImage - widthBoundingBox
    halfOfHeightDifference = int(heightDifference / 2.0)
    halfOfWidthDifference = int(widthDifference / 2.0)

    # setting the new coordinates
    linP1 = linP1 - sizeSquareImage + heightBoundingBox
    colP1 = colP1
    linP2 = linP2
    colP2 = colP2 + sizeSquareImage - widthBoundingBox

    # fine adjusting in the positions
    if (linP2 - linP1) % 32 != 0:
        linP2 += 1
    if (colP2 - colP1) % 32 != 0:
        colP2 += 1

    return linP1, colP1, linP2, colP2


# get the name of cropped image
def getCroppedBoundingBoxImageName(croppedImagesPath, originalImageName, className, idBoundingBox, objectPosition):
    return croppedImagesPath + className + "/" \
           + originalImageName + '-' + className + '-bbox-' + str(idBoundingBox) + '-' + objectPosition


# save the bounding box image
def saveCroppedBoundingBoxImage(croppedImagePathAndImageName, croppedImage):
    # croppedImageName = croppedImagePathAndImageName
    cv2.imwrite(croppedImagePathAndImageName + '.jpg', croppedImage)
    print(croppedImagePathAndImageName)


# save the bounding box image
def saveCroppedBoundingBoxAnnotationFile(croppedImageWidth, croppedImageHeight,
                                         croppedImagePathAndImageName,
                                         annotatedBoundingBox, linP1, colP1, linP2, colP2):
    # setting annotation file
    yoloAnnotationsFile = open(croppedImagePathAndImageName + '.txt', 'a+')

    # setting new bounding box in yolo format
    croppedLinP1 = annotatedBoundingBox.linPoint1 - linP1
    croppedColP1 = annotatedBoundingBox.colPoint1 - colP1
    croppedLinP2 = annotatedBoundingBox.linPoint2 - linP1
    croppedColP2 = annotatedBoundingBox.colPoint2 - colP1
    croppedBoundingBox = BoundingBox(croppedLinP1, croppedColP1, croppedLinP2, croppedColP2,
                                     annotatedBoundingBox.className)

    # getting the bounding box coordinates in  Yolo format
    linOfCentrePoint, colOfCentrePoint, widthOfCentrePoint, heightOfCentrePoint = croppedBoundingBox.getYoloAnnotation(
        croppedImageWidth, croppedImageHeight)

    # setting line to write
    line = str(DetectedObject.getValueOf(croppedBoundingBox.className)) + ' ' \
           + "{:.6f}".format(colOfCentrePoint) + ' ' \
           + "{:.6f}".format(linOfCentrePoint) + ' ' \
           + "{:.6f}".format(widthOfCentrePoint) + ' ' \
           + "{:.6f}".format(heightOfCentrePoint) \
           + LINE_FEED

    # write line
    yoloAnnotationsFile.write(line)

    # closing annotation file
    yoloAnnotationsFile.close()


# process all annotated images
def processAnnotatedImages(annotatedImagesPath, croppedImagesPath, sizeSquareImage):
    # defining counters
    totalOfImages = 0
    totalOfBoundingBoxes = 0
    totalOfExuviaBoundingBoxesImages = 0
    totalOfInstar1BoundingBoxesImages = 0
    totalOfInstar2BoundingBoxesImages = 0
    totalOfInstar3BoundingBoxesImages = 0
    totalOfInstar4BoundingBoxesImages = 0
    totalOfAdultaBoundingBoxesImages = 0
    totalOfOvoBoundingBoxesImages = 0
    # maxHeight = 0
    # maxWidth = 0

    for fileName in os.listdir(annotatedImagesPath):

        # check if file is an image or not
        if fileName.lower().find('jpg') == -1 and fileName.lower().find('jpeg') == -1:
            continue

        # get jpeg position
        jpegPosition = -1
        jpegPosition = fileName.find('jpg')
        if jpegPosition == -1: jpegPosition = fileName.find('jpeg')
        if jpegPosition == -1: jpegPosition = fileName.find('JPG')
        if jpegPosition == -1: jpegPosition = fileName.find('JPEG')

        # get only image name
        imageName = fileName[:jpegPosition - 1]

        # adding image counter
        totalOfImages += 1

        # check if processing all images of the directory
        # if len(desiredImages) > 0:
        #     # check if image name is desired or not
        #     matches = [x for x in desiredImages if x == imageName]
        #     if len(matches) == 0:
        #         continue

        # reading image
        print('')
        print('Reading image:', fileName)
        annotatedImage = cv2.imread(annotatedImagesPath + fileName)
        if annotatedImage is not None:
            # creating new file
            # jpegPosition = fileName.find('jpg') or fileName.find('jpeg')
            # id = fileName[:jpegPosition - 1]
            # id = id[1:]
            id = imageName[1:]
            annotatedImageHeight, annotatedImageWidth, annotatedImageChannel = annotatedImage.shape
            print(
                'Image: ' + imageName + "  shape: " + " height:" + str(annotatedImageHeight) + " width:" + str(
                    annotatedImageWidth))

        # open file of image annotations
        imageAnnotationsFile = open(annotatedImagesPath + imageName + ".txt", "r")

        # reading next line
        line = imageAnnotationsFile.readline()

        # defining id of bounding box
        idBoundingBox = 0

        # removing cropped images and anotations files
        # removeFilesRelatedToImage()

        # processing the file of ground truth data
        counter = 0
        while line != '':
            # increment counter
            counter += 1

            # getting the array of values
            values = line.split(' ')
            # print(values)

            idBoundingBox += 1
            imageWidth = 0
            imageHeight = 0
            idClass = int(values[0])
            colOfCentrePoint = float(values[1])
            linOfCentrePoint = float(values[2])
            heightOfCentrePoint = float(values[3])
            widthOfCentrePoint = float(values[4])

            # creating a new bounding box instance
            annotatedBoundingBox = BoundingBox(0, 0, 0, 0, '')
            annotatedBoundingBox.setYoloAnnotation(annotatedImageHeight, annotatedImageWidth, colOfCentrePoint,
                                                   linOfCentrePoint, widthOfCentrePoint, heightOfCentrePoint,
                                                   idBoundingBox,
                                                   idClass)

            # cropping bounding box
            cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage, croppedImagesPath, imageName,
                            annotatedBoundingBox.className, str(idBoundingBox),
                            'center')
            cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage, croppedImagesPath, imageName,
                            annotatedBoundingBox.className, str(idBoundingBox),
                            'north')
            cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage, croppedImagesPath, imageName,
                            annotatedBoundingBox.className, str(idBoundingBox),
                            'south')
            cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage, croppedImagesPath, imageName,
                            annotatedBoundingBox.className, str(idBoundingBox),
                            'east')
            cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage, croppedImagesPath, imageName,
                            annotatedBoundingBox.className, str(idBoundingBox),
                            'west')
            cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage, croppedImagesPath, imageName,
                            annotatedBoundingBox.className, str(idBoundingBox),
                            'northeast')
            cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage, croppedImagesPath, imageName,
                            annotatedBoundingBox.className, str(idBoundingBox),
                            'northwest')
            cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage, croppedImagesPath, imageName,
                            annotatedBoundingBox.className, str(idBoundingBox),
                            'southeast')
            cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage, croppedImagesPath, imageName,
                            annotatedBoundingBox.className, str(idBoundingBox),
                            'southwest')

            # counting total bounding boxes
            totalOfBoundingBoxes += 1

            # counting bounding boxes
            if annotatedBoundingBox.className == 'exuvia':
                totalOfExuviaBoundingBoxesImages += 1
            elif annotatedBoundingBox.className == 'instar1':
                totalOfInstar1BoundingBoxesImages += 1
            elif annotatedBoundingBox.className == 'instar2':
                totalOfInstar2BoundingBoxesImages += 1
            elif annotatedBoundingBox.className == 'instar3':
                totalOfInstar3BoundingBoxesImages += 1
            elif annotatedBoundingBox.className == 'instar4':
                totalOfInstar4BoundingBoxesImages += 1
            elif annotatedBoundingBox.className == 'adulta':
                totalOfAdultaBoundingBoxesImages += 1
            elif annotatedBoundingBox.className == 'ovo':
                totalOfOvoBoundingBoxesImages += 1

            # -----------------
            # reading next line
            # -----------------
            line = imageAnnotationsFile.readline()

        # close file
        imageAnnotationsFile.close()

    # printing statistics
    print('')
    print('Estatísticas do Processamento:')
    print('------------------------------')
    print('Total de imagens             : ', totalOfImages)
    print('Total de bounding boxes      : ', totalOfBoundingBoxes)
    print('Total de imagens de exuvia   : ', totalOfExuviaBoundingBoxesImages)
    print('Total de imagens de instar1  : ', totalOfInstar1BoundingBoxesImages)
    print('Total de imagens de instar2  : ', totalOfInstar2BoundingBoxesImages)
    print('Total de imagens de instar3  : ', totalOfInstar3BoundingBoxesImages)
    print('Total de imagens de instar4  : ', totalOfInstar4BoundingBoxesImages)
    print('Total de imagens de adultas  : ', totalOfAdultaBoundingBoxesImages)
    print('Total de imagens de ovo      : ', totalOfOvoBoundingBoxesImages)
    print('Máximo Height                : ', sizeSquareImage)
    print('Máximo Width                 : ', sizeSquareImage)
    print('')


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    print('Cropping Annotated Bounding Boxes')
    print('---------------------------------')
    print('')
    print('Input images path    : ', ANNOTATED_BOUNDING_BOXES_DATABASE_PATH)
    print('Cropped images path  : ', CROPPED_BOUNDING_BOXES_DATABASE_PATH)
    print('')
    # deleting all images of the folder
    # os.remove(CROPPED_BOUNDING_BOXES_DATABASE_PATH + "*.*")

    # setting the size square image to crop with a fixed size (height and width) used in the YOLOv4
    sizeSquareImage = 416

    # processing the annotated images
    processAnnotatedImages(ANNOTATED_BOUNDING_BOXES_DATABASE_PATH, CROPPED_BOUNDING_BOXES_DATABASE_PATH,
                           sizeSquareImage)

    # print('Total of Yolo annotations:', str(counter))
    print('End of processing')
