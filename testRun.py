from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from specialized_classes.AVCSBars import AVCSProgressBar
from kivy.clock import Clock
from base_classes.genericPlot import GenericLinePlot
from random import randint

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '600')


class TimingWindow(Screen):
    pass


class OptionsWindow(Screen):
    pass


# wm = ScreenManager()
# wm.add_widget(TimingWindow(name="timingWindow"))
# wm.add_widget(OptionsWindow(name="OptionsWindow"))

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("testrun.kv")

class testRunApp(App):
    def animate(self, dt):

        AVCSMeter1 = self.root.get_screen('timingWindow').ids.AVCS_L_IN
        AVCSMeter2 = self.root.get_screen('timingWindow').ids.AVCS_L_EX
        AVCSMeter3 = self.root.get_screen('timingWindow').ids.AVCS_R_IN
        AVCSMeter4 = self.root.get_screen('timingWindow').ids.AVCS_R_EX
        Test = self.root.get_screen('timingWindow').ids.TestLine
        #counter = float(randint(1, 10))
        #Test.add_value((counter, counter))

        if len(Test.values[0]) == 0:
            Test.add_value((1.0, 1.0))

        if AVCSMeter1.value < AVCSMeter1.max:
            AVCSMeter1.value += 1.0
            AVCSMeter2.value += 1.0
            AVCSMeter3.value += 1.0
            AVCSMeter4.value += 1.0
            number = Test.values[0][-1]
            Test.add_value((number+1, number+1))

        else:
            AVCSMeter1.value = AVCSMeter1.min
            AVCSMeter2.value = AVCSMeter2.min
            AVCSMeter3.value = AVCSMeter3.min
            AVCSMeter4.value = AVCSMeter4.min
            Test.add_value((Test.min, Test.min))



    def build(self):
        Clock.schedule_interval(self.animate, 0.1)
        return kv


if __name__ == "__main__":
    testRunApp().run()
