from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from camera.camera_function import Camera
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
import cv2


class CameraScreen(GridLayout):
    Window.fullscreen = 'auto'

    def __init__(self, back_callback=None, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        self.back_callback = back_callback

        self.cols = 1
        self.background()
        self.img1 = Image(size_hint=(1, 6))
        self.add_widget(self.img1)
        self.buttons()

        self.cam = Camera()
        self.cap = self.cam.get_camera_source()

        Clock.schedule_interval(self.update, 1.0 / 33.0)

    def update(self, dt):
        ret, frame = self.cam.show_content(self.cap)
        if ret:
            if frame.shape[1] <= 640 and frame.shape[0] <= 480:
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tostring()
                texture1 = Texture.create(size= (frame.shape[1], frame.shape[0]), colorfmt='bgr')
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


    def screen_button_work(self, instance):
        self.cam.make_screen()



    def background(self):
        with self.canvas.before:
            self.rect = Rectangle(source='../graphics/background_2.png', pos=self.pos)
            self.bind(size=self.update_background, pos=self.update_background)

    def update_background(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def buttons(self):
        button_layout = FloatLayout(size_hint=(1, 1))
        self.bind(size=self.update_background, pos=self.update_background)
        btn_back = Button(size_hint=(None, None), size=(242, 120), background_normal='../graphics/button_back.png',
                          background_down='../graphics/button_back_down.png',
                          pos_hint={'center_x': 0.2, 'center_y': 1.5})
        btn_back.bind(on_press=Clock.create_trigger(self.back_main, timeout=0.2))

        btn_make_photo = Button(size_hint=(None, None), size=(242, 120), background_normal='../graphics/button_screen.png',
                          background_down='../graphics/button_screen_down.png',
                          pos_hint={'center_x': 0.5, 'center_y': 1.5})
        btn_make_photo.bind(on_press=Clock.create_trigger(self.screen_button_work))

        btn_find_path = Button(size_hint=(None, None), size=(242, 120), background_normal='../graphics/button_back.png',
                          background_down='../graphics/button_back_down.png',
                          pos_hint={'center_x': 0.8, 'center_y': 1.5})
        btn_find_path.bind()

        button_layout.add_widget(btn_make_photo)
        button_layout.add_widget(btn_find_path)
        button_layout.add_widget(btn_back)

        self.add_widget(button_layout)

    def back_main(self, instance):
        self.clear_widgets()
        if self.back_callback:
            self.back_callback()
