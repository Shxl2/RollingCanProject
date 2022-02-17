import cv2
import numpy as np
video = cv2.VideoCapture("RollingCan.mov")
result = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*"mp4v"), 60, (640, 480))
detectedFrames = 0
totalFrames = 0

if not video.isOpened():
    print("Error opening video  file")

while video.isOpened():
    ret, frameOut = video.read()
    totalFrames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(video.get(3))
    frame_height = int(video.get(4))

    size = (frame_width, frame_height)

    if ret:

        frameGray = cv2.medianBlur(frameOut, 5)
        frameGray = cv2.cvtColor(frameGray, cv2.COLOR_BGR2GRAY)

        rows = frameGray.shape[0]
        circles = cv2.HoughCircles(frameGray, cv2.HOUGH_GRADIENT, 1, 100000000, param1 = 150, param2 = 15, minRadius = 80, maxRadius = 90)

        if circles is not None:
            detectedFrames += 1
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                # circle center
                cv2.circle(frameOut, center, 1, (0, 100, 100), 3)
                # circle outline
                radius = i[2]
                cv2.circle(frameOut, center, radius, (255, 0, 255), 3)

        frameOut = cv2.putText(frameOut, "{}/{} frames detected".format(detectedFrames, totalFrames), (600, 300), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 3, (0, 0, 0), 2, cv2.LINE_AA)

        ret, frameIn = video.read()
        try:
            Hori = np.concatenate((frameIn, frameOut), axis=1)
        except ValueError:
            break

        result.write(Hori)
        cv2.imshow("Hi", Hori)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    else:
        break

video.release()

result.release()

cv2.destroyAllWindows()
