from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from GUI.Camera_screen.Camera_work import CameraScreen
from GUI.Path_from_load_picture.Path_work import PathScreen


class ChooseScreen(FloatLayout):

    Window.fullscreen = 'auto'

    def __init__(self,back_callback=None,**kwargs):
        super(ChooseScreen, self).__init__(**kwargs)
        self.back_callback = back_callback

        self.cols = 1
        self.background()
        self.buttons()

    def background(self):
        Window.fullscreen = 'auto'

        with self.canvas.before:
            self.rect = Rectangle(source='../graphics/background_2.png', pos=self.pos)
            self.bind(size=self.update_background, pos=self.update_background)

    def update_background(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def buttons(self):
        button_layout = FloatLayout(size_hint=(1, 1))
        self.bind(size=self.update_background, pos=self.update_background)

        btn_make_photo = Button(size_hint=(None, None), size=(490, 300), background_normal='../graphics/button_take_photo.png',
                          background_down='../graphics/button_take_photo_down.png',
                          pos_hint={'center_x': 0.5, 'center_y': 0.7})
        btn_make_photo.bind(on_press=Clock.create_trigger(self.show_camera_screen, timeout=0.2))

        btn_load_picture = Button(size_hint=(None, None), size=(490, 300), background_normal='../graphics/button_load_photo.png',
                          background_down='../graphics/button_load_photo_down.png',
                          pos_hint={'center_x': 0.5, 'center_y': 0.3})
        btn_load_picture.bind(on_press=Clock.create_trigger(self.show_load_screen, timeout=0.2))

        btn_back = Button(size_hint=(None, None), size=(196, 120), background_normal='../graphics/button_back.png',
                          background_down='../graphics/button_back_down.png',
                          pos_hint={'center_x': 0.83, 'center_y': 0.17})
        btn_back.bind(on_press= Clock.create_trigger(self.back_main, timeout=0.2))

        button_layout.add_widget(btn_back)
        button_layout.add_widget(btn_load_picture)
        button_layout.add_widget(btn_make_photo)
        self.add_widget(button_layout)

    def show_camera_screen(self, instance):
        self.clear_widgets()
        camera_screen = CameraScreen(back_callback=self.show_choose_screen)
        self.add_widget(camera_screen)

    def show_load_screen(self, instance):
        self.clear_widgets()
        load_screen = PathScreen(back_callback=self.show_choose_screen)
        self.add_widget(load_screen)

    def show_choose_screen(self):
        self.clear_widgets()
        self.buttons()

    def back_main(self, instance):
        self.clear_widgets()
        if self.back_callback:
            self.back_callback()