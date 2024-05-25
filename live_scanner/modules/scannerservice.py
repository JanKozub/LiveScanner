from PIL import Image
import cv2
import numpy as np


class ScannerService:
    """
    A class used to perform various scanning operations.

    Attributes
    ----------
    video : cv2.VideoCapture or None
        Video capture object for webcam (default None)
    frameWidth : int
        Width of the video frame (default 1920)
    frameHeight : int
        Height of the video frame (default 1080)
    edgeSize : int
        Size of the edge to crop (default 0)
    oldCoordinates : list
        List to store old coordinates (default empty list)
    colorValues : list of array
        HSV color range for pen detection
    kernel : np.ndarray
        Kernel for morphological operations (default np.ones((5, 5)))
    noiseArea : int
        Minimum area to be considered as valid pen detection (default 200)
    canvas : np.ndarray
        Canvas to draw the detected pen movements (default None)
    penCords : tuple
        Coordinates of the pen (default (0, 0))
    penColor : tuple
        Color of the pen (default [255, 0, 0])

    Methods
    -------
    preProcessing(image: Image):
        Preprocesses the image to find edges.
    getCornerPoints(image: Image):
        Finds the corner points of the largest contour.
    getWarp(image: Image, pageCoordinates: np.ndarray):
        Warps the image based on the given coordinates.
    setPerspective(image: Image, cords: np.ndarray):
        Sets the perspective transform for the image.
    postProcess(image: Image):
        Post-processes the image by rotating and cropping edges.
    processImage(image: Image):
        Processes the image to find and warp the largest contour.
    getPenFromImage(image: Image):
        Detects the pen in the image and draws its movement on the canvas.
    startScanner():
        Starts the video capture for scanning.
    stopScanner():
        Stops the video capture.
    getFinalImage():
        Gets the final processed image with pen movements.
    getColorsImage(lower: np.ndarray, higher: np.ndarray):
        Gets the image filtered by the specified HSV color range.
    mergeImages(bottomLayer: Image, topLayer: Image):
        Merges two images with alpha blending.
    """

    def __init__(self, colorValues: [np.array, np.array]):
        """
        :param colorValues:
            Color values of detected pen(default read from file)
        """

        self.video: cv2.VideoCapture | None = None
        self.frameWidth: int = 1920
        self.frameHeight: int = 1080
        self.edgeSize: int = 0
        self.oldCoordinates: list = []
        self.colorValues: [np.array, np.array] = colorValues
        self.kernel: np.ndarray = np.ones((5, 5))
        self.noiseArea: int = 200
        self.canvas: np.array = None
        self.penCords: tuple[int, int] = (0, 0)
        self.penColor: tuple[int, int, int] = (255, 0, 0)

    def preProcessing(self, image: Image):
        """
        Preprocesses the image to find edges.

        Parameters
        ----------
        :param image : Image
            The input image.

        Returns
        -------
        :return np.ndarray
            The preprocessed image with edges detected.
        """

        imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Gray image
        imgBlur = cv2.GaussianBlur(imgGray, (1, 1), 1)  # Blur Image - easing edges
        imgCanny = cv2.Canny(imgBlur, 100, 300)  # Canny Image - canny algo to find edges

        # extending the found edges and then eroding it to smoothen the image
        imgDilate = cv2.dilate(imgCanny, self.kernel, iterations=2)
        imgErode = cv2.erode(imgDilate, self.kernel, iterations=1)
        return imgErode

    @staticmethod
    def getCornerPoints(image: Image):
        """
        Finds the corner points of the largest contour.

        Parameters
        ----------
        :param image : Image
            The input image.

        Returns
        -------
        :return np.ndarray
            The corner points of the largest contour.
        """

        cornerPointsOfMaxArea = np.array([])
        maxArea = 0
        contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100000:  # area in px x px
                peri = cv2.arcLength(cnt, True)  # perimeter of the closed shape
                cornerPoints = cv2.approxPolyDP(cnt, 0.01 * peri, True)
                if area > maxArea and len(cornerPoints) == 4:
                    cornerPointsOfMaxArea = cornerPoints
                    maxArea = area

        return cornerPointsOfMaxArea

    def getWarp(self, image: Image, pageCoordinates: np.ndarray):
        """
        Warps the image based on the given coordinates.

        Parameters
        ----------
        :param image : Image
            The input image.
        :param pageCoordinates : np.ndarray
            The coordinates for warping the image.

        Returns
        -------
        :return Image
            The warped image.
        """

        if not pageCoordinates.any():  # when object's perimeter is partly covered
            prev_coord_points = self.oldCoordinates[:]

            if len(prev_coord_points) < 1:
                return image

            image = self.setPerspective(image, prev_coord_points)
        else:
            new_coord_points = np.reshape(pageCoordinates, (4, 2))
            self.oldCoordinates = new_coord_points[:]

            image = self.setPerspective(image, new_coord_points)

        return image

    def setPerspective(self, image: Image, cords: np.ndarray):
        """
        Sets the perspective transform for the image.

        Parameters
        ----------
        :param image : Image
            The input image.
        :param cords : np.ndarray
            The coordinates for perspective transform.

        Returns
        -------
        :return Image
            The perspective transformed image.
        """

        pts1 = np.float32([cords[1], cords[0], cords[2], cords[3]])
        pts2 = np.float32([[0, 0], [self.frameWidth, 0], [0, self.frameHeight], [self.frameWidth, self.frameHeight]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        return cv2.warpPerspective(image, matrix, (self.frameWidth, self.frameHeight))

    def postProcess(self, image: Image):
        """
        Post-processes the image by rotating and cropping edges.

        Parameters
        ----------
        :param image : Image
            The input image.

        Returns
        -------
        :return np.ndarray
            The post-processed image.
        """

        rotatedImage = cv2.rotate(image, cv2.ROTATE_180)
        return rotatedImage[self.edgeSize:rotatedImage.shape[0] - self.edgeSize,
                            self.edgeSize:rotatedImage.shape[1] - self.edgeSize]

    def processImage(self, image: Image):
        """
        Processes the image to find and warp the largest contour.

        Parameters
        ----------
        :param image : Image
            The input image.

        Returns
        -------
        :return np.ndarray
            The processed image.
        """

        imgPreprocessed = self.preProcessing(image)
        contours = self.getCornerPoints(imgPreprocessed)
        imgWarp = self.getWarp(image, contours)
        return self.postProcess(imgWarp)

    def getPenFromImage(self, image: Image):
        """
        Detects the pen in the image and draws its movement on the canvas.

        Parameters
        ----------
        :param image : Image
            The input image.

        Returns
        -------
        :return np.ndarray
            The canvas with pen movements drawn.
        """

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, self.colorValues[0], self.colorValues[1])
        mask = cv2.erode(mask, self.kernel, iterations=1)
        mask = cv2.dilate(mask, self.kernel, iterations=2)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours and cv2.contourArea(max(contours, key=cv2.contourArea)) > self.noiseArea:
            c = max(contours, key=cv2.contourArea)
            x2, y2, w, h = cv2.boundingRect(c)
            x2 = 1920 - x2
            y2 = 1080 - y2

            if self.penCords[0] != 0 or self.penCords[1] != 0:
                self.canvas = cv2.line(self.canvas, self.penCords, (x2, y2), self.penColor, 6)

            self.penCords = (x2, y2)

        return self.canvas

    def startScanner(self):
        """
        Starts the video capture for scanning.
        """

        self.video = cv2.VideoCapture(0)
        self.video.set(3, self.frameWidth)
        self.video.set(4, self.frameHeight)
        self.video.set(100, 150)
        self.canvas = np.zeros_like(self.video.read()[1])

    def stopScanner(self):
        """
        Stops the video capture.
        """

        cv2.destroyAllWindows()
        self.video = None

    def getFinalImage(self):
        """
        Gets the final processed image with pen movements.

        Returns
        -------
        :return np.ndarray
            The final image with pen movements.
        """

        image = self.video.read()[1]
        processedImage = self.processImage(image)
        return self.getPenFromImage(processedImage)

    def getColorsImage(self, lower: np.ndarray, higher: np.ndarray):
        """
        Gets the image filtered by the specified HSV color range.

        Parameters
        ----------
        :param lower : np.ndarray
            Lower HSV color range.
        :param higher : np.ndarray
            Higher HSV color range.
        """

        image = self.video.read()[1]

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        res = cv2.bitwise_and(image, image, mask=cv2.inRange(hsv, lower, higher))

        return res

    @staticmethod
    def mergeImages(bottomLayer: Image, topLayer: Image):
        """
        Merges two images with alpha blending.

        Parameters
        ----------
        :param bottomLayer : Image
            The bottom image layer.
        :param topLayer : Image
            The top image layer.

        Returns
        -------
        :return np.ndarray
            The merged image with alpha blending.
        """

        bottomLayer = cv2.cvtColor(np.array(bottomLayer), cv2.COLOR_RGB2RGBA)
        topLayer = cv2.cvtColor(np.array(topLayer), cv2.COLOR_RGB2RGBA)

        topLayer = cv2.resize(topLayer, (bottomLayer.shape[1], bottomLayer.shape[0]))
        return cv2.addWeighted(bottomLayer, 1, topLayer, 1, 0.0)
