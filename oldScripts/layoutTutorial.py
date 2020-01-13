
##Creating a grid layout and populating it with buttons
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class MyGrid(GridLayout):
    #kwargs means we don't know how many arguments we may receive
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 1 # Defines the number of overall cols to 1

        #Creates a subsetted grid layout
        self.inside=GridLayout()
        self.inside.cols=2

        #Exists in the interior gridlayout
        #########---------------------------------------#########
        #Lets add label widget
        self.inside.add_widget(Label(text="First Name: "))
        self.name = TextInput(multiline=False) #text input box
        self.inside.add_widget(self.name) # add text input to gui

        #Lets add more to get a true grid
        self.inside.add_widget(Label(text="Last Name: "))
        self.lastName = TextInput(multiline=False)
        self.inside.add_widget(self.lastName)

        self.inside.add_widget(Label(text="Email: "))
        self.email = TextInput(multiline=False)
        self.inside.add_widget(self.email)
        ########----------------------------------------##########
        self.add_widget(self.inside)
        
        self.submit = Button(text="Submit", font_size=40)
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)

    #Adding action if pressed or not
    def pressed(self, instance):
        #get inputs
        name = self.name.text
        last = self.lastName.text
        email = self.email.text

        #print inputs
        print("Name:", name, "\nLast Name:", last, "\nEmail:", email)

        #reset inputs
        self.name.text=""
        self.lastName.text=""
        self.email.text=""
        
class MyApp(App):
    def build(self):
        return(MyGrid())

if __name__ == "__main__":
    MyApp().run()
