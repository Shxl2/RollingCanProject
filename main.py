import cv2
import numpy as np
video = cv2.VideoCapture("RollingCan.mov")

if not video.isOpened():
    print("Error opening video  file")

while video.isOpened():
    ret, frameIn = video.read()



    if ret:
        frameOut = cv2.medianBlur(frameIn, 5)
        frameOut = cv2.cvtColor(frameOut, cv2.COLOR_BGR2GRAY)

        rows = frameOut.shape[0]
        circles = cv2.HoughCircles(frameOut, cv2.HOUGH_GRADIENT, 1, rows / 8, param1=70, param2=17, minRadius=90, maxRadius=100)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                # circle center
                cv2.circle(frameIn, center, 1, (0, 100, 100), 3)
                # circle outline
                radius = i[2]
                cv2.circle(frameIn, center, radius, (255, 0, 255), 3)
        cv2.imshow('Frame', frameIn)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    else:
        break

video.release()

cv2.destroyAllWindows()
