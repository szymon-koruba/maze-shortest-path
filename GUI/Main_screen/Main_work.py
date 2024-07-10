from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from GUI.Guide_screen.Guide_work import GuideScreen


class MainScreen(GridLayout):

    Window.fullscreen = 'auto'

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.cols = 1
        self.background()
        self.buttons()

    def background(self):
        with self.canvas.before:
            self.rect = Rectangle(source='../graphics/background.png', pos=self.pos)
            self.bind(size=self.update_background, pos=self.update_background)

    def update_background(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def buttons(self):
        button_layout = FloatLayout(size_hint=(1, 1))
        self.bind(size=self.update_background, pos=self.update_background)

        btn_start = Button(size_hint=(None, None), size=(422, 200), background_normal='../graphics/button_start.png',
                           background_down='../graphics/button_start_down.png',
                           pos_hint={'center_x': 0.5, 'center_y': 0.6})
        btn_start.bind()

        btn_settings = Button(size_hint=(None, None), size=(422, 200),
                              background_normal='../graphics/button_settings.png',
                              background_down='../graphics/button_settings_down.png',
                              pos_hint={'center_x': 0.5, 'center_y': 0.4})
        btn_settings.bind()

        btn_guide = Button(size_hint=(None, None), size=(422, 200), background_normal='../graphics/button_guide.png',
                           background_down='../graphics/button_guide_down.png',
                           pos_hint={'center_x': 0.5, 'center_y': 0.2})
        btn_guide.bind(on_press=Clock.create_trigger(self.show_guide_screen, timeout=0.2))

        btn_exit = Button(size_hint=(None, None), size=(242, 120), background_normal='../graphics/button_exit.png',
                          background_down='../graphics/button_exit_down.png',
                          pos_hint={'center_x': 0.83, 'center_y': 0.17})
        btn_exit.bind(on_press=Clock.create_trigger(self.exit_app, timeout=0.2))

        button_layout.add_widget(btn_start)
        button_layout.add_widget(btn_settings)
        button_layout.add_widget(btn_guide)
        button_layout.add_widget(btn_exit)

        self.add_widget(button_layout)

    def exit_app(self, instance):
        App.get_running_app().stop()

    def show_guide_screen(self, instance):
        self.clear_widgets()
        guide_screen = GuideScreen(back_callback=self.show_main_screen)
        self.add_widget(guide_screen)

    def show_main_screen(self):
        self.clear_widgets()
        self.buttons()


class MyApp(App):
    def build(self):
        return MainScreen()


MyApp().run()
