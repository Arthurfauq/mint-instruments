import kivy
import pyaudio
import wave
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

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
CHUNK = 512
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "test.wav"

class HomeScreen(Screen):
    pass


class MenuScreen(Screen):
    pass


class RecordScreen(Screen):
    def __init__(self, **kwargs):
        super(RecordScreen, self).__init__(**kwargs)

    def record_audio(self):
        audio = pyaudio.PyAudio()

        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        print "recording..."
        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print "Finished recording !"

        stream.stop_stream()
        stream.close()
        audio.terminate()

        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()


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
        root.add_widget(RecordScreen(name='Record'))
        return root


if __name__ == "__main__":
    MintApp().run()
