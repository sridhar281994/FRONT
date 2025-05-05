import requests
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.clock import Clock
from video_call_launcher import launch_video_call 

BACKEND_URL = "https://kivyapp.onrender.com"


class VideoChatScreen(Screen):
    chat_timer = None
    search_event = None
    session_timer = None
    session_timeout_seconds = 120  # 2 minutes

    def on_enter(self):
        self.start_matchmaking()
        self.start_session_timer()

    def on_leave(self):
        if self.chat_timer:
            self.chat_timer.cancel()
            self.chat_timer = None
        if self.search_event:
            self.search_event.cancel()
            self.search_event = None
        if self.session_timer:
            self.session_timer.cancel()
            self.session_timer = None

    def start_matchmaking(self):
        user_data = App.get_running_app().user_data
        if not user_data:
            self.ids.status.text = "User data missing."
            return
        self.user_id = user_data.get("id")
        self.gender = user_data.get("gender")
        self.ids.status.text = "Searching for a match..."
        # First call only once to /start-chat/
        try:
            response = requests.post(
                f"{BACKEND_URL}/start-chat/",
                json={"user_id": self.user_id, "gender": self.gender}
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("matched_with"):
                    App.get_running_app().matched_user_id = data["matched_with"]
                    self.ids.status.text = f"Matched with user {data['matched_with']}!"
                    self.cancel_session_timer()
                    self.show_match_popup(data["matched_with"])
                    self.enable_chat_ui()
                else:
                    # If no match yet, start polling /check-my-match/
                    self.search_event = Clock.schedule_interval(self.poll_check_match, 5)
            else:
                self.ids.status.text = "Server error."
        except Exception as e:
            self.ids.status.text = f"Error: {e}"

    def poll_check_match(self, dt):
        try:
            response = requests.post(
                f"{BACKEND_URL}/check-my-match/",
                json={"user_id": self.user_id}
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("matched_with"):
                    App.get_running_app().matched_user_id = data["matched_with"]
                    self.ids.status.text = f"Matched with user {data['matched_with']}!"
                    if self.search_event:
                        self.search_event.cancel()
                        self.search_event = None
                    self.cancel_session_timer()
                    self.show_match_popup(data["matched_with"])
                    self.enable_chat_ui()
                else:
                    self.ids.status.text = "Waiting for match..."
            else:
                self.ids.status.text = "Server error."
        except Exception as e:
            self.ids.status.text = f"Error: {e}"

    def show_match_popup(self, matched_user_id):
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text=f"Matched with user ID {matched_user_id}!"))
        close_btn = Button(text="OK", size_hint_y=None, height="40dp")
        box.add_widget(close_btn)
        popup = Popup(title="Match Found", content=box, size_hint=(0.7, 0.3))
        close_btn.bind(on_release=lambda *args: (popup.dismiss(), self.generate_agora_token_and_join()))
        popup.open()

    def generate_agora_token_and_join(self):
        try:
            user_id = App.get_running_app().user_data.get("id")
            response = requests.post(f"{BACKEND_URL}/generate-token/", params={"user_id": user_id})
            if response.status_code == 200:
                data = response.json()
                channel_name = data["channel_name"]
                token = data["token"]
                print(f"Agora Channel: {channel_name}, Token: {token}")
                launch_video_call(channel_name, token)  # Native SDK launcher
            else:
                print("Failed to generate Agora Token:", response.text)
        except Exception as e:
            print("Agora Token generation error:", e)

    def stop_search(self):
        user_id = App.get_running_app().user_data.get("id")
        if user_id:
            try:
                response = requests.delete(f"{BACKEND_URL}/match-queue/{user_id}")
                if response.status_code == 200:
                    self.ids.status.text = "Search stopped."
                else:
                    self.ids.status.text = "Failed to stop search."
            except Exception as e:
                self.ids.status.text = f"Error: {e}"

    def enable_chat_ui(self):
        self.ids.chat_input.disabled = False
        self.ids.send_button.disabled = False
        self.ids.mic_button.opacity = 1
        self.start_point_deduction()

    def start_point_deduction(self):
        if self.chat_timer:
            self.chat_timer.cancel()
        self.chat_timer = Clock.schedule_interval(self.deduct_points, 60)

    def deduct_points(self, dt):
        app = App.get_running_app()
        current_points = app.user_data.get("wallet_points", 0)
        if current_points >= 25:
            app.user_data["wallet_points"] = current_points - 25
            print(f"Deducted 25 points. Remaining: {app.user_data['wallet_points']}")
        else:
            self.ids.status.text = "Insufficient points. Ending chat."
            self.end_chat()

    def end_chat(self):
        if self.chat_timer:
            self.chat_timer.cancel()
        if self.search_event:
            self.search_event.cancel()
        if self.session_timer:
            self.session_timer.cancel()
        App.get_running_app().matched_user_id = None
        self.manager.current = "home_screen"

    def start_session_timer(self):
        if self.session_timer:
            self.session_timer.cancel()
        self.session_timer = Clock.schedule_once(self.session_timeout_reached, self.session_timeout_seconds)

    def cancel_session_timer(self):
        if self.session_timer:
            self.session_timer.cancel()
            self.session_timer = None

    def session_timeout_reached(self, dt):
        self.stop_search()
        self.ids.status.text = "Session expired. Please try again."
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text="Session expired. Try again."))
        ok_button = Button(text="OK", size_hint_y=None, height="40dp")
        layout.add_widget(ok_button)
        popup = Popup(title="Session Timeout", content=layout, size_hint=(0.7, 0.3))
        ok_button.bind(on_release=lambda *args: (popup.dismiss(), setattr(self.manager, 'current', "home_screen")))
        popup.open()

    def send_message(self):
        message = self.ids.chat_input.text.strip()
        if message:
            self.ids.chat_log.text += f"\nYou: {message}"
            App.get_running_app().chat_history.append(f"You: {message}")
            self.ids.chat_input.text = ""
            app = App.get_running_app()
            if "chat_history" not in app.user_data:
                app.user_data["chat_history"] = []
            app.user_data["chat_history"].append(f"You: {message}")