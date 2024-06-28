import cv2
def getting_full_photo():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Frame', frame)

        if ret and cv2.waitKey(1) & 0xFF == ord(' '):
            screen = (cv2.imwrite('screen.jpg', frame))
            return screen
