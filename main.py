import cv2
import numpy as np
video = cv2.VideoCapture("RollingCan.mov")
result = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*"mp4v"), 20.0, (3840, 1080))
detectedFrames = 0

if not video.isOpened():
    print("Error opening video  file")

while video.isOpened():
    ret, frameOut = video.read()
    ret, frameIn = video.read()
    totalFrames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

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
                cv2.circle(frameOut, center, 10, (0, 0, 0), -1)
                # circle outline
                radius = i[2]
                cv2.circle(frameOut, center, radius, (0, 255, 0), 3)

        frameOut = cv2.putText(frameOut, "{}/{} frames detected".format(detectedFrames, totalFrames), (600, 300), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 3, (0, 0, 0), 2, cv2.LINE_AA)
        frameOut = cv2.putText(frameOut, "Output", (900, 100), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 3, (0, 0, 0), 2,
                               cv2.LINE_AA)

        frameIn = cv2.putText(frameIn, "Input", (900, 100), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 3, (0, 0, 0), 2,
                              cv2.LINE_AA)

        try:
            combinedImage = np.concatenate((frameIn, frameOut), axis=1)
        except ValueError:
            break

        result.write(combinedImage)

        cv2.imshow("RollingCanProject", combinedImage)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    else:
        break

video.release()

result.release()

cv2.destroyAllWindows()
