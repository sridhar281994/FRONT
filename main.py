from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from login_register import RegisterScreen, LoginScreen, ProfileUpdateScreen
from screens.video_chat_screen import VideoChatScreen
from screens.settings_screen import SettingsScreen
from screens.home_screen import HomeScreen
from screens.welcome_screen import WelcomeScreen
from screens.chat_history_screen import ChatHistoryScreen


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_data = {}
        self.matched_user_id = None
        self.gender_preference = None  # Defaults to None, means "Any"
        self.chat_history = []

    def attempt_gender_preference_change(self):
        if self.user_data.get("wallet_points", 0) < 25:
            popup = Popup(
                title="Not Enough Points",
                content=Label(text="You have less than 25 points"),
                size_hint=(0.7, 0.3)
            )
            popup.open()
        else:
            self.show_gender_preference_popup()

    def show_gender_preference_popup(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        label = Label(text="Choose your preferred gender")
        btn_male = Button(text="Male")
        btn_female = Button(text="Female")
        btn_any = Button(text="Any")
        popup = Popup(title="Gender Preference", content=layout, size_hint=(0.75, 0.5))

        def set_pref(pref):
            self.gender_preference = pref if pref else None
            popup.dismiss()
            if self.root:
                home = self.root.get_screen("home_screen")
                if home.ids.get("gender_pref_button"):
                    label_text = "Pref: {}".format(pref.capitalize()) if pref else "Male/Female"
                    home.ids.gender_pref_button.text = label_text

        btn_male.bind(on_release=lambda *a: set_pref("male"))
        btn_female.bind(on_release=lambda *a: set_pref("female"))
        btn_any.bind(on_release=lambda *a: set_pref(None))
        layout.add_widget(label)
        layout.add_widget(btn_male)
        layout.add_widget(btn_female)
        layout.add_widget(btn_any)
        popup.open()

    def build(self):
        Builder.load_file("ui/screens.kv")
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="welcome_screen"))
        sm.add_widget(HomeScreen(name="home_screen"))
        sm.add_widget(RegisterScreen(name="register_screen"))
        sm.add_widget(LoginScreen(name="login_screen"))
        sm.add_widget(ProfileUpdateScreen(name="profile_update_screen"))
        sm.add_widget(VideoChatScreen(name="video_chat_screen"))
        sm.add_widget(SettingsScreen(name="settings_screen"))
        sm.add_widget(ChatHistoryScreen(name="chat_history_screen"))
        return sm


if __name__ == "__main__":
    MyApp().run()
