from kivy.uix.screenmanager import Screen
from kivy.app import App


class ChatHistoryScreen(Screen):
    def on_pre_enter(self):
        app = App.get_running_app()
        chat_history = app.user_data.get("chat_history", [])
        history_text = "\n".join(chat_history)
        self.ids.history_log.text = history_text if history_text else "No chats yet."
