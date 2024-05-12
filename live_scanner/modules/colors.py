import cv2
import numpy as np


def nothing(x):
    pass


cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

cv2.namedWindow("Trackbars")

cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    colorValues = [np.array([l_h, l_s, l_v]), np.array([u_h, u_s, u_v])]

    res = cv2.bitwise_and(frame, frame, mask=cv2.inRange(hsv, colorValues[0], colorValues[1]))

    cv2.imshow('Trackbars', cv2.resize(res, None, fx=1, fy=1))

    key = cv2.waitKey(1)
    if key == 27:
        break

    if key == ord('s'):
        thearray = [[l_h, l_s, l_v], [u_h, u_s, u_v]]
        print(thearray)

        np.save('vals', thearray)
        break

cap.release()
cv2.destroyAllWindows()
