from kivy.uix.screenmanager import Screen
from kivy.app import App


class WelcomeScreen(Screen):
    def on_pre_enter(self):
        # This updates wallet points when screen is shown
        user_data = App.get_running_app().user_data
        wallet = user_data.get("wallet_points", 0)
        if "wallet_points_label" in self.ids:
            self.ids.wallet_points_label.text = f"Wallet: {wallet} points"