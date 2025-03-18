from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from camera.camera_function import Camera
from GUI.Path_from_photo.Path_work_from_photo import PathScreen
from GUI.resource_graphics import resource_path as rp
import cv2
import os


class CameraScreen(GridLayout):
    Window.fullscreen = 'auto'

    def __init__(self, back_callback=None, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        self.back_callback = back_callback

        self.cols = 1
        self.background()

        self.cam = Camera()
        if self.cam.get_camera_source() is not None:
            self.camera_available()
            self.cap = self.cam.get_camera_source()
            self.buttons_with_camera()
            Clock.schedule_interval(self.update, 1.0 / 33.0)
        else:
            self.camera_not_available()
            self.buttons_without_camera()

    def update(self, dt):
        ret, frame = self.cam.show_content(self.cap)
        if ret:
            if frame.shape[1] <= 640 and frame.shape[0] <= 480:
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tostring()
                texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.img1.texture = texture1
            elif frame.shape[1] >= 640 and frame.shape[0] >= 480:
                cropped_image = frame[(frame.shape[0]-480):frame.shape[0], (frame.shape[1]-640):frame.shape[1]]
                buf1 = cv2.flip(cropped_image, 0)
                buf = buf1.tostring()
                texture1 = Texture.create(colorfmt='bgr')
                texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.img1.texture = texture1
            return frame

    def camera_available(self):
        camera_layout = FloatLayout(size_hint=(1, 1))
        self.img1 = Image(pos_hint={'center_x': 0.5, 'center_y': 0.1})
        camera_layout.add_widget(self.img1)
        self.add_widget(camera_layout)

    def screen_button_work(self, instance):
        self.cam.make_screen()

    def background(self):
        with self.canvas.before:
            self.rect = Rectangle(source=rp('assets/background_2.png'), pos=self.pos)
            self.bind(size=self.update_background, pos=self.update_background)

    def update_background(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def buttons_without_camera(self):
        button_layout = FloatLayout(size_hint=(1, 1))
        self.bind(size=self.update_background, pos=self.update_background)
        btn_back = Button(size_hint=(None, None), size=(196, 120),
                          background_normal=rp('assets/button_back.png'),
                          background_down=rp('assets/button_back_down.png'),
                          pos_hint={'center_x': 0.2, 'center_y': 0.4})
        btn_back.bind(on_press=Clock.create_trigger(self.back_main, timeout=0.2))

        button_layout.add_widget(btn_back)

        self.add_widget(button_layout)

    def buttons_with_camera(self):
        button_layout = FloatLayout(size_hint=(1, 1))
        self.bind(size=self.update_background, pos=self.update_background)
        btn_back = Button(size_hint=(None, None), size=(196, 120),
                          background_normal=rp('assets/button_back.png'),
                          background_down=rp('assets/button_back_down.png'),
                          pos_hint={'center_x': 0.2, 'center_y': 0.4})
        btn_back.bind(on_press=Clock.create_trigger(self.back_main, timeout=0.2))

        btn_make_photo = Button(size_hint=(None, None), size=(245, 150),
                                background_normal=rp('assets/button_screen.png'),
                                background_down=rp('assets/button_screen_down.png'),
                                pos_hint={'center_x': 0.5, 'center_y': 0.4})
        btn_make_photo.bind(on_press=Clock.create_trigger(self.screen_button_work))

        btn_find_path = Button(size_hint=(None, None), size=(245, 150),
                               background_normal=rp('assets/button_load_photo.png'),
                               background_down=rp('assets/button_load_photo_down.png'),
                               pos_hint={'center_x': 0.8, 'center_y': 0.4})
        btn_find_path.bind(on_press=Clock.create_trigger(self.show_path_screen))

        button_layout.add_widget(btn_find_path)
        button_layout.add_widget(btn_back)
        button_layout.add_widget(btn_make_photo)

        self.add_widget(button_layout)

    def camera_not_available(self):
        picture_layout = FloatLayout(size_hint=(1, 1))
        img = Image(size=(200, 200), pos_hint={'center_x': 0.5, 'center_y': 0.2},
                    source=rp('assets/no_signal_picture.png'))
        picture_layout.add_widget(img)
        self.add_widget(picture_layout)

    def show_path_screen(self, instance):
        self.clear_widgets()
        path_screen = PathScreen(back_callback=self.show_camera_screen)
        self.add_widget(path_screen)

    def show_camera_screen(self):
        self.clear_widgets()

        self.cam = Camera()
        if self.cam.get_camera_source() is not None:
            self.cap.release()
            self.camera_available()
            self.cap = self.cam.get_camera_source()
            self.buttons_with_camera()
            Clock.schedule_interval(self.update, 1.0 / 33.0)
        else:
            self.camera_not_available()
            self.buttons_without_camera()

    def back_main(self, instance):
        self.clear_widgets()
        if self.back_callback:
            self.back_callback()
