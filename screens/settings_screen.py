from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import requests

BACKEND_URL = "https://kivyapp.onrender.com"


class SettingsScreen(Screen):
    def on_pre_enter(self):
        self.load_settings()

    def load_settings(self):
        app = App.get_running_app()
        user_data = app.user_data
        if not user_data:
            return
        self.ids.display_name_input.text = user_data.get("nickname", "")
        self.ids.description_input.text = user_data.get("description", "")
        self.ids.upi_input.text = user_data.get("upi_id", "")
        self.ids.wallet_points_label.text = f"Wallet: {user_data.get('wallet_points', 0)} points"
        profile_photo = user_data.get("profile_photo")
        if profile_photo:
            self.ids.profile_image.source = profile_photo
        else:
            self.ids.profile_image.source = "assets/default.png"

    def choose_photo(self):
        layout = BoxLayout(orientation='vertical')
        filechooser = FileChooserIconView()
        select_button = Button(text="Select", size_hint_y=None, height="48dp")
        popup = Popup(title="Choose Profile Photo", content=layout, size_hint=(0.9, 0.9))
        layout.add_widget(filechooser)
        layout.add_widget(select_button)

        def select_file(instance):
            selected = filechooser.selection
            if selected:
                self.ids.profile_image.source = selected[0]
                App.get_running_app().user_data["profile_photo"] = selected[0]
                popup.dismiss()

        select_button.bind(on_release=select_file)
        popup.open()

    def save_settings(self):
        app = App.get_running_app()
        user_data = app.user_data
        nickname = self.ids.display_name_input.text
        description = self.ids.description_input.text
        upi_id = self.ids.upi_input.text
        profile_photo = user_data.get("profile_photo", "")
        if not nickname or not upi_id:
            popup = Popup(
                title="Missing Fields",
                content=Label(text="Nickname and UPI ID are required!"),
                size_hint=(0.7, 0.3)
            )
            popup.open()
            return
        user_data["nickname"] = nickname
        user_data["description"] = description
        user_data["upi_id"] = upi_id
        user_data["profile_photo"] = profile_photo
        # Update to backend
        try:
            response = requests.post(
                f"{BACKEND_URL}/save-settings",
                json={
                    "user_id": user_data.get("id"),
                    "nickname": nickname,
                    "description": description,
                    "upi_id": upi_id,
                    "profile_photo": profile_photo
                }
            )
            if response.status_code == 200:
                popup = Popup(
                    title="Success",
                    content=Label(text="Settings saved successfully!"),
                    size_hint=(0.7, 0.3)
                )
                popup.open()
            else:
                popup = Popup(
                    title="Error",
                    content=Label(text="Failed to save settings!"),
                    size_hint=(0.7, 0.3)
                )
                popup.open()
        except Exception as e:
            popup = Popup(
                title="Error",
                content=Label(text=f"Error: {e}"),
                size_hint=(0.7, 0.3)
            )
            popup.open()

    def recharge_wallet(self):
        amount_text = self.ids.recharge_amount_input.text.strip()
        if not amount_text.isdigit():
            popup = Popup(
                title="Invalid Amount",
                content=Label(text="Please enter a valid amount"),
                size_hint=(0.7, 0.3)
            )
            popup.open()
            return
        amount = int(amount_text)
        app = App.get_running_app()
        user_id = app.user_data.get("id")
        try:
            response = requests.post(
                f"{BACKEND_URL}/generate-upi-intent",
                json={"user_id": user_id, "amount": amount}
            )
            data = response.json()
            if "upi_intent_url" in data:
                import webbrowser
                webbrowser.open(data["upi_intent_url"])
            else:
                popup = Popup(
                    title="Error",
                    content=Label(text="Failed to generate UPI intent"),
                    size_hint=(0.7, 0.3)
                )
                popup.open()
        except Exception as e:
            popup = Popup(
                title="Error",
                content=Label(text=f"Error: {e}"),
                size_hint=(0.7, 0.3)
            )
            popup.open()
