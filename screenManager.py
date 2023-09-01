from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from libs.baseclass.welcome import WelcomeScreen
from libs.baseclass.login import LoginScreen
from libs.baseclass.signup import SignUpScreen
from libs.baseclass.settings import SettingsScreen
from libs.baseclass.createpost import CreatePost



class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.add_widget(Builder.load_file('libs/kvs/welcome.kv'))
        self.add_widget(Builder.load_file('libs/kvs/main.kv'))
        self.add_widget(Builder.load_file('libs/kvs/settings.kv'))
        self.add_widget(Builder.load_file('libs/kvs/signup.kv'))
        self.add_widget(Builder.load_file('libs/kvs/login.kv'))
        self.add_widget(Builder.load_file('libs/kvs/profile.kv'))
        self.add_widget(Builder.load_file('libs/kvs/post_page.kv'))
        self.add_widget(Builder.load_file('libs/kvs/commentSection.kv'))




