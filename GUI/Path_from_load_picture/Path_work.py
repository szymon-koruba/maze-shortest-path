from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.image import Image
from GUI.Path_from_load_picture.full_b_from_load_picture import CreatePath
from GUI.resource_graphics import resource_path as rp
from threading import Thread
import os


class PathScreen(FloatLayout):

    def __init__(self, back_callback=None, **kwargs):
        super(PathScreen, self).__init__(**kwargs)
        self.back_callback = back_callback
        self.background()
        self.create_buttons()
        self.image_layout = FloatLayout(size_hint=(1, None), height=Window.height - 120)
        self.add_widget(self.image_layout)
        self.image_widget = None
        if self.image_widget is not None:
            self.update_image(None)

    def background(self):
        Window.fullscreen = 'auto'
        with self.canvas.before:
            self.rect = Rectangle(source=rp('assets/background_2.png'), pos=self.pos)
            self.bind(size=self.update_background, pos=self.update_background)

    def update_background(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def create_buttons(self):
        button_layout = FloatLayout(size_hint=(1, None), height=120)
        button_layout.pos_hint = {'x': 0, 'y': 0}

        btn_path = Button(size_hint=(None, None), size=(245, 150),
                          background_normal=rp('assets/button_load_photo.png'),
                          background_down=rp('assets/button_load_photo_down.png'),
                          pos_hint={'center_x': 0.5, 'center_y': 1.8})
        btn_path.bind(on_press=Clock.create_trigger(self.full_function_works, timeout=0.2))

        btn_back = Button(size_hint=(None, None), size=(196, 120),
                          background_normal=rp('assets/button_back.png'),
                          background_down=rp('assets/button_back_down.png'),
                          pos_hint={'center_x': 0.83, 'center_y': 1.5})
        btn_back.bind(on_press=Clock.create_trigger(self.back_main, timeout=0.2))

        button_layout.add_widget(btn_back)
        button_layout.add_widget(btn_path)

        self.add_widget(button_layout)

    def full_function_works(self, instance):
        def load_image():
            cp = CreatePath()
            image_path = cp.full_path_load_pict()
            Clock.schedule_once(lambda dt: self.update_image(image_path), 0)

        thread = Thread(target=load_image)
        thread.start()

    def update_image(self, image_path):
        if self.image_widget:
            self.image_widget.source = image_path
        else:
            self.image_widget = Image(size=(600, 600), size_hint=(None, None),
                                     pos_hint={'center_x': 0.5, 'center_y': 0.6},
                                     source=image_path)
            self.image_layout.add_widget(self.image_widget)


    def back_main(self, instance):
        self.clear_widgets()
        if self.back_callback:
            self.back_callback()
