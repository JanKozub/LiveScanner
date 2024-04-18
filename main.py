import cv2 as cv

cap = cv.VideoCapture(1)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

print("Camera opened")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    canny = cv.Canny(gray, 100, 200)

    contours, _ = cv.findContours(canny.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    color = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)

    cv.drawContours(color, contours, -1, (0, 255, 0), 3)

    cv.imshow('output', color)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()