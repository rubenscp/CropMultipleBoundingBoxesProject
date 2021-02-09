# from Entity.BoundingBox import BoundingBox


# Image  Class
import cv2

from Entity.BoundingBox import BoundingBox


class Image:
    def __init__(self, id, originalImage, originalHeight, originalWidth, originalChannel, checkedImage, checkedHeight,
                 checkedWidth, checkedChannel, imageFileName, locationPath, originalBoundingBoxesList,
                 checkedBoundingBoxesList):
        self.id = id

        self.originalImage = originalImage
        self.originalHeight = originalHeight
        self.originalWidth = originalWidth
        self.originalChannel = originalChannel

        self.checkedImage = checkedImage
        self.checkedHeight = checkedHeight
        self.checkedWidth = checkedWidth
        self.checkedChannel = checkedChannel

        self.imageFileName = imageFileName
        self.locationPath = locationPath
        self.originalBoundingBoxesList = originalBoundingBoxesList
        self.checkedBoundingBoxesList = checkedBoundingBoxesList

    def toString(self):
        # originalHeight, originalWidth, originalChannel = image.shape
        text = str(self.id) + ' ' + self.imageFileName + ' ' + self.locationPath
        # 'Image size: ' + 'height: ' + str(originalHeight) + '  width:' + str(originalWidth) + '  channel:' + str(
        #     originalChannel) + '  ' \
        # + str(len(self.boundingBoxesList))
        return text

    def calculateBoundingBoxesPointsForOriginalImage(self, ORIGINAL_IMAGES_DATABASE_PATH):
        # loading the original image
        self.setOriginalImage(ORIGINAL_IMAGES_DATABASE_PATH)

        # initializing the bounding boxes list of original image
        self.originalBoundingBoxesList = []

        # calculating  the bounding boxes list of original image
        for checkedBoundingBox in self.checkedBoundingBoxesList:
            # creating a new bounding box instance
            originalBoundingBox = BoundingBox()

            # defining the class name of bounding box
            originalBoundingBox.className = checkedBoundingBox.className

            # calculating the new coordinates of the two points
            originalBoundingBox.linPoint1 = self.calculateOriginalCoordinate(checkedBoundingBox.linPoint1,
                                                                             self.checkedHeight,
                                                                             self.originalHeight)
            originalBoundingBox.colPoint1 = self.calculateOriginalCoordinate(checkedBoundingBox.colPoint1,
                                                                             self.checkedWidth,
                                                                             self.originalWidth)
            originalBoundingBox.linPoint2 = self.calculateOriginalCoordinate(checkedBoundingBox.linPoint2,
                                                                             self.checkedHeight,
                                                                             self.originalHeight)
            originalBoundingBox.colPoint2 = self.calculateOriginalCoordinate(checkedBoundingBox.colPoint2,
                                                                             self.checkedWidth,
                                                                             self.originalWidth)

            # appending bounding box object to list
            self.originalBoundingBoxesList.append(originalBoundingBox)

        # removing  the original image from object to avoid insuficient memory problem
        self.removeOriginalImage()

    def calculateOriginalCoordinate(self, currentCoordinate, checkedDimension, originalDimension):
        # percentOfCheckedImage = currentCoordinate * 100.0 / checkedDimension
        # newCoordinate = int(originalDimension * percentOfCheckedImage / 100.0)
        newCoordinate = int((currentCoordinate / (checkedDimension * 1.0)) * originalDimension)
        return newCoordinate

    def setCheckedImage(self, CHECKED_IMAGES_DATABASE_PATH):
        checkedImage = cv2.imread(CHECKED_IMAGES_DATABASE_PATH + self.imageFileName)
        checkedHeight, checkedWidth, checkedChannel = checkedImage.shape
        self.checkedImage = checkedImage
        self.checkedHeight = checkedHeight
        self.checkedWidth = checkedWidth
        self.checkedChannel = checkedChannel

    def removeCheckedImage(self):
        self.checkedImage = None

    def setOriginalImage(self, ORIGINAL_IMAGES_DATABASE_PATH):
        originalImage = cv2.imread(ORIGINAL_IMAGES_DATABASE_PATH + self.imageFileName)
        originalHeight, originalWidth, originalChannel = originalImage.shape
        self.originalImage = originalImage
        self.originalHeight = originalHeight
        self.originalWidth = originalWidth
        self.originalChannel = originalChannel

    def removeOriginalImage(self):
        self.originalImage = None
        self.originalHeight = None
        self.originalWidth = None
        self.originalChannel = None
