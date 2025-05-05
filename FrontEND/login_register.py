import os
import hashlib
import requests
from kivy.uix.screenmanager import Screen
from kivy.app import App
from plyer import filechooser
from PIL import Image

BACKEND_URL = "https://kivyapp.onrender.com"


class RegisterScreen(Screen):
    def choose_photo(self):
        filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        if selection:
            self.ids.photo_input.text = selection[0]

    def register(self):
        email_or_phone = self.ids.email_input.text
        nickname = self.ids.nickname_input.text
        description = self.ids.description_input.text
        password = self.ids.password_input.text
        gender = self.ids.gender_spinner.text
        image_path = self.ids.photo_input.text
        if not all([email_or_phone, nickname, password, gender]):
            print("Missing required fields")
            return
        dest_path = ""
        if image_path and os.path.exists(image_path):
            filename = os.path.basename(image_path)
            dest_path = os.path.join("assets/profile_pics", filename)
            try:
                img = Image.open(image_path)
                img = img.convert("RGB")
                img = img.resize((300, 300))
                img.save(dest_path, format='JPEG', quality=70)
                print("Profile photo resized and saved.")
            except Exception as e:
                print("Image processing error:", e)
                return
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            response = requests.post(
                f"{BACKEND_URL}/register",
                json={
                    "email_or_phone": email_or_phone,
                    "nickname": nickname,
                    "description": description,
                    "password_hash": password_hash,
                    "gender": gender,
                    "profile_photo": dest_path
                }
            )
            if response.status_code == 200:
                print("Registration successful")
                self.manager.current = "login_screen"
            else:
                print("Registration failed:", response.text)
        except Exception as e:
            print("Error during registration:", e)


class LoginScreen(Screen):
    def login(self):
        email_or_phone = self.ids.login_email_input.text
        password = self.ids.login_password_input.text
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            response = requests.post(
                f"{BACKEND_URL}/login",
                json={"email_or_phone": email_or_phone, "password_hash": password_hash}
            )
            if response.status_code == 200:
                user = response.json()
                print("Login successful:", user['nickname'])
                App.get_running_app().user_data = user
                # Default preference on login
                App.get_running_app().gender_preference = "Any"
                self.manager.current = "home_screen"
            else:
                print("Login failed:", response.text)
        except Exception as e:
            print("Login request error:", e)


class ProfileUpdateScreen(Screen):
    def choose_new_photo(self):
        filechooser.open_file(on_selection=self.handle_photo_selection)

    def handle_photo_selection(self, selection):
        if selection:
            self.ids.new_photo_input.text = selection[0]

    def update_photo(self):
        image_path = self.ids.new_photo_input.text
        if not image_path or not os.path.exists(image_path):
            print("Please select a valid image file.")
            return
        try:
            filename = os.path.basename(image_path)
            dest_path = os.path.join("assets/profile_pics", filename)
            img = Image.open(image_path)
            img = img.convert("RGB")
            img = img.resize((300, 300))
            img.save(dest_path, format='JPEG', quality=70)
            user_data = App.get_running_app().user_data
            user_data['profile_photo'] = dest_path
            print("Profile photo updated locally.")
        except Exception as e:
            print("Error updating profile photo:", e)
