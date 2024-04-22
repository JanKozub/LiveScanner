import cv2
import numpy as np

video = cv2.VideoCapture(1)  # WebCam
frameWidth = 1920
frameHeight = 1080

video.set(3, frameWidth)
video.set(4, frameHeight)
video.set(100, 150)

store_coordinate_points = []

def preProcessing(image):
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Gray image
    imgBlur = cv2.GaussianBlur(imgGray, (1, 1), 1)  # Blur Image - easing edges
    imgCanny = cv2.Canny(imgBlur, 100, 300)  # Canny Image - canny algo to find edges
    kernel = np.ones((5, 5))
    imgDilate = cv2.dilate(imgCanny, kernel, iterations=2) # extending the found edges and then eroding it to smoothen the image
    imgErode = cv2.erode(imgDilate, kernel, iterations=1)

    return imgErode

def getContours(image): # find the biggest area inside contours to find the white paper
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


def getWarp(image, page_coord_points):
    global store_coordinate_points

    if not coord_points.any():  # when object's perimeter is partly covered
        prev_coord_points = store_coordinate_points[:]

        if len(prev_coord_points) < 1:
            return image

        image = setPerspective(image, prev_coord_points)
    else:
        new_coord_points = np.reshape(page_coord_points, (4, 2))
        store_coordinate_points = new_coord_points[:]

        image = setPerspective(image, new_coord_points)

    return image


def setPerspective(image, cords):
    pts1 = np.float32([cords[1], cords[0], cords[2], cords[3]])
    pts2 = np.float32([[0, 0], [frameWidth, 0], [0, frameHeight], [frameWidth, frameHeight]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    return cv2.warpPerspective(image, matrix, (frameWidth, frameHeight))


while True:
    success, img = video.read()

    imgPreprocessed = preProcessing(img)
    coord_points = getContours(imgPreprocessed)

    imgWarp = getWarp(img, coord_points)

    img_rotate_by_180 = cv2.rotate(imgWarp, cv2.ROTATE_180)

    cv2.imshow("Video", img_rotate_by_180)

    if cv2.waitKey(10) & 0xFF == ord(' '):
        break
