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
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import AsyncImage
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from glob import glob
from os.path import dirname, join, basename

WIDTH = 2
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
CHUNK = 512
WAVE_OUTPUT_FILENAME = "test.wav"
choix_utilisateur = 0
choix_utilisateur_bis = 0

class HomeScreen(Screen):
    pass


class BackButton(FloatLayout):
    pass


class MenuScreen(Screen):
    pass


class Tracks(Screen):
    pass


class ChooseInstruOne(Screen):
    def saveinstru(self):
        global choix_utilisateur
        choix_utilisateur = self.ids.carousel.index
        print("Test de recuperation index instrument :",choix_utilisateur)


class RecordingOne(Screen):
    record_button = ObjectProperty(None)
    button_text = StringProperty()

    def __init__(self, **kwargs):
        super(RecordingOne, self).__init__(**kwargs)
        self.button_text = "Record"
        global audio
        global waveFile
        global stream
        audio = pyaudio.PyAudio()

    def callback(self, in_data, frame_count, time_info, status):
        if self.record_button.state == "down":
            waveFile.writeframes(in_data)
            return (in_data, pyaudio.paContinue)
        elif self.record_button.state == "normal":
            waveFile.close()
            return (in_data, pyaudio.paComplete)

    def start_record(self):
        global stream
        global waveFile
        stream = audio.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            stream_callback=self.callback,
                            frames_per_buffer=512)

        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setframerate(RATE)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))

        stream.start_stream()

    def toggle_audio(self, null):
        global playButton
        global finishButton

        if playButton.state == "down":
            playButton.text = "Stop"
            self.play_audio()

        elif playButton.state == "normal":
            playButton.text = "Play"
            self.stop_audio()

    def stop_record(self):
        global stream
        global audio
        global playButton
        global finishButton

        stream.stop_stream()
        stream.close()
        audio.terminate()

        self.record_button.__setattr__('pos_hint', {'center_x': .38, 'y': .5})
        playButton = ToggleButton(
            text='Play',
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={'center_x': .62, 'y': .5})
        finishButton = ToggleButton(
            text='Edit',
            size_hint=(None, None),
            size=(100, 40),
            pos_hint={'right': .97, 'y': .25}
        )
        playButton.bind(on_press=self.toggle_audio)
        self.ids.layout2.add_widget(playButton)
        self.ids.layout2.add_widget(finishButton)

    def play_audio(self):
        global stream
        global p

        p = pyaudio.PyAudio()
        wavef = wave.open('test.wav', 'rb')

        stream = p.open(
            format = p.get_format_from_width(wavef.getsampwidth()),
            channels = wavef.getnchannels(),
            rate = wavef.getframerate(),
            output = True)

        data = wavef.readframes(CHUNK)

        while len(data) > 0:
            stream.write(data)
            data = wavef.readframes(CHUNK)

    def stop_audio(self):
        global stream
        global p

        stream.stop_stream()
        stream.close()
        p.terminate()

    def record_audio(self):
        self.affichageinstru()

        if self.record_button.state == "down":
            self.button_text = "Stop"
            self.start_record()
            self.ids.layout2.clear_widgets()

        elif self.record_button.state == "normal":
            self.button_text = "New"
            self.stop_record()

    def affichageinstru(self):
        global choix_utilisateur
        global img
        if choix_utilisateur == 0:
            img = AsyncImage(source='img/micro.png', size_hint=(.2, .2) ,
                             pos_hint={'center_x':.1, 'center_y': .5})
        if choix_utilisateur == 1:
            img = AsyncImage(source='img/piano.png', size_hint=(.2, .2) ,
                             pos_hint={'center_x':.1, 'center_y': .5})
        if choix_utilisateur == 2:
            img = AsyncImage(source='img/guitarelec.png', size_hint=(.2, .2) ,
                             pos_hint={'center_x':.1, 'center_y': .5})
        if choix_utilisateur == 3:
            img = AsyncImage(source='img/guitaraccoustic.png', size_hint=(.2, .2) ,
                             pos_hint={'center_x':.1, 'center_y': .5})
        if choix_utilisateur == 4:
            img = AsyncImage(source='img/batterie.png', size_hint=(.2, .2) ,
                             pos_hint={'center_x':.1, 'center_y': .5})
        self.ids.layout1.add_widget(img)

    def removeinstru(self):
        self.ids.layout1.clear_widgets()


class ChooseInstruTwo(Screen):
    def saveinstrudouble(self):
        global choix_utilisateur
        global choix_utilisateur_bis
        choix_utilisateur = self.ids.firsttrack.index
        print("Test de recuperation index instrument 1 :",choix_utilisateur)
        choix_utilisateur_bis = self.ids.secondtrack.index
        print("Test de recuperation index instrument 2 :", choix_utilisateur_bis)


class RecordingTwo(Screen):
    def affichageinstrudouble(self):
        global choix_utilisateur
        global choix_utilisateur_bis
        global img
        global img_bis
        print("Choix utilisateur", choix_utilisateur, " et ", choix_utilisateur_bis)
        if choix_utilisateur == 0:
            img = AsyncImage(source='img/micro.png', size_hint=(.2, .2) ,
                             pos_hint={'center_x':.1, 'center_y': .65})
        if choix_utilisateur == 1:
            img = AsyncImage(source='img/piano.png', size_hint=(.2, .2) ,
                             pos_hint={'center_x':.1, 'center_y': .65})
        if choix_utilisateur == 2:
            img = AsyncImage(source='img/guitarelec.png', size_hint=(.2, .2) ,
                             pos_hint={'center_x':.1, 'center_y': .65})
        if choix_utilisateur == 3:
            img = AsyncImage(source='img/guitaraccoustic.png', size_hint=(.2, .2) ,
                             pos_hint={'center_x':.1, 'center_y': .65})
        if choix_utilisateur == 4:
            img = AsyncImage(source='img/batterie.png', size_hint=(.2, .2) ,
                             pos_hint={'center_x':.1, 'center_y': .65})
        self.add_widget(img)

        if choix_utilisateur_bis == 0:
            img_bis = AsyncImage(source='img/micro.png', size_hint=(.2, .2) ,
                                 pos_hint={'center_x':.1, 'center_y': .35})
        if choix_utilisateur_bis == 1:
            img_bis = AsyncImage(source='img/piano.png', size_hint=(.2, .2) ,
                                 pos_hint={'center_x':.1, 'center_y': .35})
        if choix_utilisateur_bis == 2:
            img_bis = AsyncImage(source='img/guitarelec.png', size_hint=(.2, .2) ,
                                 pos_hint={'center_x':.1, 'center_y': .35})
        if choix_utilisateur_bis == 3:
            img_bis = AsyncImage(source='img/guitaraccoustic.png', size_hint=(.2, .2) ,
                                 pos_hint={'center_x':.1, 'center_y': .35})
        if choix_utilisateur_bis == 4:
            img_bis = AsyncImage(source='img/batterie.png', size_hint=(.2, .2) ,
                                 pos_hint={'center_x':.1, 'center_y': .35})
        self.add_widget(img_bis)


    def removeinstrudouble(self):
        global img
        global img_bis
        self.remove_widget(img)
        self.remove_widget(img_bis)


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
    global curdir
    global audio
    audio = pyaudio.PyAudio()
    curdir = dirname(__file__)
    style = ObjectProperty(None)
    volume = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PadScreen, self).__init__(**kwargs)
        self.load_styles()

    def load_styles(self):
        for name in glob(join(curdir, 'sounds/pad/styles', '*')):
            styleName = basename(name).capitalize()
            self.ids.style.values.append(styleName)

    def load_sounds(self):
        self.release_audio()
        self.ids.sl.clear_widgets()
        for name in glob(join(curdir, 'sounds/pad/styles/' + self.ids.style.text.lower(), '*.wav')):
            pad_button = AudioButton(
                text=basename(name[:-4]).replace('_', ' '),
                filename=name)
            self.ids.sl.add_widget(pad_button)

    def release_audio(self):
        for audiobutton in self.ids.sl.children:
            audiobutton.release_audio()

    def set_volume(self, value):
        self.volume.text =  str(round(value*100, 0)).replace('.0', '%')
        for audiobutton in self.ids.sl.children:
            audiobutton.set_volume(value)


class MintApp(App):
    def build(self):
        root = ScreenManager()
        root.add_widget(HomeScreen(name='Home'))
        root.add_widget(MenuScreen(name='Menu'))
        root.add_widget(ProductionScreen(name='Production'))
        root.add_widget(PadScreen(name='Pad'))
        root.add_widget(Tracks(name='Tracks'))
        root.add_widget(ChooseInstruOne(name='InstruOne'))
        root.add_widget(ChooseInstruTwo(name='InstruTwo'))
        root.add_widget(RecordingOne(name='RecordOne'))
        root.add_widget(RecordingTwo(name='RecordTwo'))
        return root

if __name__ == "__main__":
    MintApp().run()
