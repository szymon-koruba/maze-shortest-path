import cv2
import os


class Camera:
    def __init__(self):
        self.cap = None
        self.ret = None
        self.frame = None
        self.screenshot_counter = 0

    def get_camera_source(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.cap = None

    def turn_off_camera(self):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()
            return True
        return False

    def show_content(self):
        self.ret, self.frame = self.cap.read()
        cv2.imshow('Frame', self.frame)

    def make_screen(self):
        if self.ret and cv2.waitKey(1) & 0xFF == ord(' '):
            filename = f'screen_{self.screenshot_counter}.jpg'
            screen = (cv2.imwrite(filename, self.frame))
            self.screenshot_counter += 1
            self.screen_save(screen, filename)
            return screen, filename

    def full_part(self):
        self.get_camera_source()
        while True:
            self.show_content()
            self.make_screen()
            self.turn_off_camera()

    def screen_save(self, screen, file_name):
        if screen:
            folder_path = os.path.join(os.getcwd(), 'screens')
            os.makedirs(folder_path, exist_ok=True)
            file_path = os.path.join(folder_path, file_name)
            os.rename(file_name, file_path)
            return file_path
