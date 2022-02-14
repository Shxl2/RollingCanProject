import cv2

video = cv2.VideoCapture("RollingCan.mov")

if not video.isOpened():
    print("Error opening video  file")

while video.isOpened():
    ret, frame = video.read()

    if ret:
        cv2.imshow('Frame', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    else:
        break

video.release()

cv2.destroyAllWindows()
