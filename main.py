from GUI.Main_screen.Main_work import MainScreen
from kivy.app import App

class MyApp(App):
    def build(self):
        return MainScreen()

MyApp().run()
