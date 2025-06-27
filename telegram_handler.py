from pyrogram import Client
import config

class TelegramHandler:
    def __init__(self):
        self.app = Client("session1", api_id=config.api_id, api_hash=config.api_hash)
        self.app.start()
        self.app.send_message(config.chat_name, "/start")

    def send_photo(self, photo_path):
        self.app.send_photo(config.chat_name, photo_path)

    def delete_messages(self):
        for message in self.app.iter_history(config.chat_name, limit=15):
            self.app.delete_messages(config.chat_name, message.message_id)

    def get_last_message(self):
        for message in self.app.iter_history(config.chat_name, limit=1):
            return message
