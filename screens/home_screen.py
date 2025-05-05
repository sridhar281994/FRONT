from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class HomeScreen(Screen):
    def on_pre_enter(self):
        user = App.get_running_app().user_data
        if self.ids.get("wallet_points_label"):
            self.ids.wallet_points_label.text = f"Wallet: {user.get('wallet_points', 0)} points"
        if self.ids.get("gender_pref_btn"):
            pref = user.get("preferred_gender", "Any")
            self.ids.gender_pref_btn.text = f"Preferred: {pref}"

    def show_gender_preference_popup(self):
        app = App.get_running_app()
        user_data = app.user_data
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(text="Choose your preferred gender:")
        box.add_widget(label)
        btn_male = Button(text="Male", size_hint_y=None, height=40)
        btn_female = Button(text="Female", size_hint_y=None, height=40)
        btn_any = Button(text="Any", size_hint_y=None, height=40)
        btn_cancel = Button(text="Cancel", size_hint_y=None, height=40)
        popup = Popup(title="Set Preference", content=box, size_hint=(0.8, 0.5))

        def set_preference(gender):
            if gender in ["Male", "Female"]:
                if user_data.get("wallet_points", 0) >= 25:
                    user_data["preferred_gender"] = gender
                    user_data["wallet_points"] -= 25
                    self.ids.gender_pref_btn.text = f"Preferred: {gender}"
                    self.ids.wallet_points_label.text = f"Wallet: {user_data['wallet_points']} points"
                    print(f"Preference set to {gender}")
                    popup.dismiss()
                else:
                    label.text = "You need at least 25 points"
            elif gender == "Any":
                user_data.pop("preferred_gender", None)
                self.ids.gender_pref_btn.text = "Preferred: Any"
                print("Preference reset to Any")
                popup.dismiss()

        btn_male.bind(on_release=lambda *_: set_preference("Male"))
        btn_female.bind(on_release=lambda *_: set_preference("Female"))
        btn_any.bind(on_release=lambda *_: set_preference("Any"))
        btn_cancel.bind(on_release=popup.dismiss)
        box.add_widget(btn_male)
        box.add_widget(btn_female)
        box.add_widget(btn_any)
        box.add_widget(btn_cancel)
        popup.open()