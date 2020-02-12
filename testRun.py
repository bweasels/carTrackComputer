from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from oldScripts.AVCSDials import AVCSProgressBar
from kivy.clock import Clock

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '600')

class TimingWindow(Screen):
    pass

class OptionsWindow(Screen):
    pass

#wm = ScreenManager()
#wm.add_widget(TimingWindow(name="timingWindow"))
#wm.add_widget(OptionsWindow(name="OptionsWindow"))

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("testrun.kv")

class testRunApp(App):
    def animate(self, dt):
        bar = self.root.get_screen('timingWindow').ids.AVCS_L_In
        bar2 = self.root.get_screen('timingWindow').ids.AVCS_L_Ex
        if bar.value < bar.max:
            bar.value += 1
            bar2.value += 1
        else:
            bar.value = bar.min
            bar2.value=bar2.min
    
    def build(self):
        Clock.schedule_interval(self.animate, 0.05)
        return kv

if __name__ == "__main__":
    testRunApp().run()
