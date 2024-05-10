import cv2
import numpy as np

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

kernel = np.ones((5, 5), np.uint8)
canvas = np.zeros_like(cap.read()[1])
markerColors = (np.array([95, 130, 90]), np.array([180, 255, 255]))
penColor = [255, 0, 0]
x1, y1 = 0, 0
noiseArea = 800

while 1:
    frame = cv2.flip(cap.read()[1], 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, markerColors[0], markerColors[1])
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours and cv2.contourArea(max(contours, key=cv2.contourArea)) > noiseArea:
        c = max(contours, key=cv2.contourArea)
        x2, y2, w, h = cv2.boundingRect(c)

        if x1 != 0 or y1 != 0:
            canvas = cv2.line(canvas, (x1, y1), (x2, y2), penColor, 10)

        x1, y1 = x2, y2

    frame = cv2.addWeighted(frame, 1.0, canvas, 1.0, 0.0)
    cv2.imshow('Trackbars', cv2.resize(np.hstack((canvas, frame)), None, fx=1, fy=1))

    k = cv2.waitKey(1) & 0xFF
    if k == ord("e"):
        break

    if k == ord('c'):
        canvas = np.zeros_like(cap.read()[1])

cv2.destroyAllWindows()
cap.release()
