from kivy.app import App
from kivy.graphics import Line, Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.text import Label
from kivy.lang.builder import Builder
from kivy.clock import Clock
from collections.abc import Iterable
from math import ceil
from dials import CircularProgressBar

#class RootWidget(FloatLayout):
#
#    def __init__(self, **kwargs):
#        # make sure we aren't overriding any important functionality
#        super(RootWidget, self).__init__(**kwargs)

#        # let's add a Widget to this layout
#        self.add_widget(
#            Button(text="Hello World",
#                   size_hint=(.1, .1),
#                   pos_hint={'center_x': .1, 'center_y': .3}))

class MainApp(App):

    def animate(self, dt):
        for bar in self.root.children[:-1]:
            if bar.value < bar.max:
                bar.value += 1
            else:
                bar.value = bar.min

    def build(self):
        dial = CircularProgressBar()
        #btn = Button(text ="Push Me !",
        #             font_size ="20sp",
        #             background_color = (1, 1, 1, 1),
        #             color = (1, 1, 1, 1),
        #             size = (32, 32),
        #             size_hint = (.2, .2),
        #             pos = (300, 250))
        #btn.bind(on_press = self.callback)
        #return btn
        return dial
    def callback(self, event):
        print("button pressed")
        print("You'll get another interview :)")

root = MainApp()

root.run()
#        Clock.schedule_interval(self.animate, 0.05)
#        with root.canvas.before:
#            self.rect = Rectangle(size=root.size, pos=root.pos, source='images/FA20Engine3.png')
#            return root
#        self.root = root = RootWidget()
#        root.bind(size=self._update_rect, pos=self._update_rect)

#        with root.canvas.before:
#            Color(1, 1, 1, 1)  # green; colors range from 0-1 not 0-255
#            self.rect = Rectangle(size=root.size, pos=root.pos, source='images/FA20Engine3.png')
#        return root

#    def _update_rect(self, instance, value):
#        self.rect.pos = instance.pos
#        self.rect.size = instance.size

if __name__ == '__main__':
    MainApp().run()
