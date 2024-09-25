import cv2
import os
from datetime import datetime


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
        return self.ret, self.frame

    def make_screen(self):
        c = datetime.now()
        a = c.date()
        self.filename = f'screen_{self.screenshot_counter}_{a}.jpg'
        self.screen = (cv2.imwrite(self.filename, self.frame))
        self.screenshot_counter += 1
        self.screen_save()

    def screen_save(self):
        if self.screen:
            folder_path = os.path.join(os.getcwd(), 'screens')
            file_path = os.path.join(folder_path, self.filename)
            os.rename(self.filename, file_path)
