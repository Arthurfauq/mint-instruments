import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from glob import glob
from os.path import dirname, join, basename


class HomeScreen(Screen):
    pass


class MenuScreen(Screen):
    pass


class ProductionScreen(Screen):
    pass


class IconButton(ButtonBehavior, Image):
    pass


class CustomDropDown(DropDown):
    pass


class AudioButton(Button):
    filename = StringProperty(None)
    sound = ObjectProperty(None, allownone=True)
    volume = NumericProperty(1.0)

    def on_press(self):
        if self.sound is None:
            self.sound = SoundLoader.load(self.filename)
        # stop the sound if it's currently playing
        if self.sound.status != 'stop':
            self.sound.stop()
        self.sound.volume = self.volume
        self.sound.play()

    def release_audio(self):
        if self.sound:
            self.sound.stop()
            self.sound.unload()
            self.sound = None

    def set_volume(self, volume):
        self.volume = volume
        if self.sound:
            self.sound.volume = volume


class PadScreen(Screen):
    def __init__(self, **kwargs):
        super(PadScreen, self).__init__(**kwargs)
        curdir = dirname(__file__)

        for name in glob(join(curdir, 'sounds/pad/styles', '*')):
            style = basename(name).capitalize()
            self.ids.styles.values.append(style)

        for name in glob(join(curdir, 'sounds/pad/instruments/drums_percussions', '*.wav')):
            pad_button = AudioButton(
                text=basename(name[:-4]).replace('_', ' '),
                filename=name)
            self.ids.sl.add_widget(pad_button)

    def release_audio(self):
        for audiobutton in self.ids.sl.children:
            audiobutton.release_audio()

    def set_volume(self, value):
        for audiobutton in self.ids.sl.children:
            audiobutton.set_volume(value)


class MintApp(App):
    def build(self):
        root = ScreenManager()
        root.add_widget(HomeScreen(name='Home'))
        root.add_widget(MenuScreen(name='Menu'))
        root.add_widget(ProductionScreen(name='Production'))
        root.add_widget(PadScreen(name='Pad'))
        return root

if __name__ == "__main__":
    MintApp().run()
