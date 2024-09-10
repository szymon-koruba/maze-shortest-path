from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.image import Image


class GuideScreen(FloatLayout):

    Window.fullscreen = 'auto'

    def __init__(self,back_callback=None,**kwargs):
        super(GuideScreen, self).__init__(**kwargs)
        self.back_callback = back_callback

        self.cols = 1
        self.background()
        self.guide_tekst()
        self.buttons()

    def background(self):

        with self.canvas.before:
            self.rect = Rectangle(source='../graphics/background_2.png', pos=self.pos)
            self.bind(size=self.update_background, pos=self.update_background)

    def update_background(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def guide_tekst(self):
        img = Image(size_hint=(2, 1),size=(200, 200), pos_hint={'center_x': 0.8, 'center_y': 0.2}, source='../graphics/gate.jpg')
        self.add_widget(img)

    def buttons(self):
        button_layout = FloatLayout(size_hint=(1, 1))
        self.bind(size=self.update_background, pos=self.update_background)

        btn_back = Button(size_hint=(None, None), size=(242, 120), background_normal='../graphics/button_back.png',
                          background_down='../graphics/button_back_down.png',
                          pos_hint={'center_x': 0.7, 'center_y': 0.1})
        btn_back.bind(on_press= Clock.create_trigger(self.back_main, timeout=0.2))

        button_layout.add_widget(btn_back)

        self.add_widget(button_layout)

    def back_main(self, instance):
        self.clear_widgets()
        if self.back_callback:
            self.back_callback()

