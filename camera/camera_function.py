import cv2
import os


class Camera:
    def __init__(self):
        self.ret = None
        self.frame = None
        self.screenshot_counter = 0
        self.screen = None
        self.filename = None
        self.ix = -1
        self.iy = -1
        self.drawing = False
        self.x, self.y, self.w, self.h = 100, 100, 200, 200


    def get_camera_source(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = None
        return cap

    def show_content(self, cap):
        self.ret, self.frame = cap.read()
        cv2.imshow('Obraz', self.frame)
        return self.ret, self.frame

    def make_screen(self):
        self.filename = f'screen_{self.screenshot_counter}.jpg'
        self.screen = (cv2.imwrite(self.filename, self.frame))
        self.screenshot_counter += 1
        self.screen_save()

    def screen_save(self):
        if self.screen:
            folder_path = os.path.join(os.getcwd(), 'screens')
            os.makedirs(folder_path, exist_ok=True)
            file_path = os.path.join(folder_path, self.filename)
            os.rename(self.filename, file_path)

    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy = x, y

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                self.w = x - self.ix
                self.h = y - self.iy

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.w = x - self.ix
            self.h = y - self.iy
