import cv2
import numpy as np


class Scanner:
    def __init__(self):
        self.frameWidth = 1920
        self.frameHeight = 1080
        self.edgeSize = 50
        self.old_coordinate_points = []

        self.video = cv2.VideoCapture(1)
        self.video.set(3, self.frameWidth)
        self.video.set(4, self.frameHeight)
        self.video.set(100, 150)

        self.current_image = self.video.read()

    @staticmethod
    def preProcessing(image):
        imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Gray image
        imgBlur = cv2.GaussianBlur(imgGray, (1, 1), 1)  # Blur Image - easing edges
        imgCanny = cv2.Canny(imgBlur, 100, 300)  # Canny Image - canny algo to find edges
        kernel = np.ones((5, 5))
        imgDilate = cv2.dilate(imgCanny, kernel,
                               iterations=2)  # extending the found edges and then eroding it to smoothen the image
        imgErode = cv2.erode(imgDilate, kernel, iterations=1)

        return imgErode

    @staticmethod
    def getContours(image):  # find the biggest area inside contours to find the white paper
        biggest = np.array([])
        maxArea = 0
        contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100000:  # area in px x px
                peri = cv2.arcLength(cnt, True)  # perimeter of the closed shape
                cornerPoints = cv2.approxPolyDP(cnt, 0.01 * peri, True)
                if area > maxArea and len(cornerPoints) == 4:
                    biggest = cornerPoints
                    maxArea = area

        return biggest

    def getWarp(self, image, page_coord_points):
        if not page_coord_points.any():  # when object's perimeter is partly covered
            prev_coord_points = self.old_coordinate_points[:]

            if len(prev_coord_points) < 1:
                return image

            image = self.setPerspective(image, prev_coord_points)
        else:
            new_coord_points = np.reshape(page_coord_points, (4, 2))
            self.old_coordinate_points = new_coord_points[:]

            image = self.setPerspective(image, new_coord_points)

        return image

    def setPerspective(self, image, cords):
        pts1 = np.float32([cords[1], cords[0], cords[2], cords[3]])
        pts2 = np.float32([[0, 0], [self.frameWidth, 0], [0, self.frameHeight], [self.frameWidth, self.frameHeight]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        return cv2.warpPerspective(image, matrix, (self.frameWidth, self.frameHeight))

    def postProcess(self, image):
        rotatedImage = cv2.rotate(image, cv2.ROTATE_180)
        return rotatedImage[
               self.edgeSize:rotatedImage.shape[0] - self.edgeSize,
               self.edgeSize:rotatedImage.shape[1] - self.edgeSize]  # cropping unclear edges

    def processImage(self, image):
        imgPreprocessed = self.preProcessing(image)
        contours = self.getContours(imgPreprocessed)
        imgWarp = self.getWarp(image, contours)
        return self.postProcess(imgWarp)

    @staticmethod
    def getWritingFromImage(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mask = cv2.bitwise_not(cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1])
        return cv2.bitwise_and(gray, gray, mask=mask)

    def startScanner(self):
        # image1 = cv2.imread('screenshot.png')
        # image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)

        while True:
            image = self.video.read()[1]
            processedImage = self.processImage(image)
            writing = self.getWritingFromImage(processedImage)
            cv2.imshow("Video", writing)

            # writing = writing[0:image1.shape[0], 0: image1.shape[1]]
            # mergedImages = cv2.addWeighted(image1, 0.5, writing, 0.5, 0.0)
            # cv2.imshow("Video", mergedImages)

            if cv2.waitKey(10) & 0xFF == ord(' '):
                break


scanner = Scanner()
scanner.startScanner()
