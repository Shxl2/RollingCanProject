import cv2
import numpy as np
video = cv2.VideoCapture("RollingCan.mov")
counter = 0
if not video.isOpened():
    print("Error opening video  file")

while video.isOpened():
    ret, frameIn = video.read()

    if ret:
        frameOut = frameIn
        frameGray = cv2.medianBlur(frameIn, 5)
        frameGray = cv2.cvtColor(frameGray, cv2.COLOR_BGR2GRAY)

        rows = frameGray.shape[0]
        circles = cv2.HoughCircles(frameGray, cv2.HOUGH_GRADIENT, 1, rows / 8, param1=70,
                                   param2=17, minRadius=80, maxRadius=90)

        if circles is not None:
            counter += 1
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                # circle center
                cv2.circle(frameGray, center, 1, (0, 100, 100), 3)
                # circle outline
                radius = i[2]
                cv2.circle(frameGray, center, radius, (255, 0, 255), 3)

        frameOut = cv2.putText(frameGray, "{} frames detected".format(counter), (400, 300), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 0), 2, cv2.LINE_AA)

        cv2.imshow('Frame', frameGray)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    else:
        break

video.release()

cv2.destroyAllWindows()
