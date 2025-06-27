import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
import config

class VkHandler:
    def __init__(self, main_app):
        self.app = main_app
        self.vk_session = vk_api.VkApi(token=config.token)
        self.session_api = self.vk_session.get_api()
        self.longpoll = VkLongPoll(self.vk_session)
        self.upload = VkUpload(self.vk_session)

    def send_message(self, user_id, message, keyboard=None, attachment=None):
        post = {
            "user_id": user_id,
            "message": message,
            "random_id": 0,
        }
        if keyboard:
            post["keyboard"] = keyboard.get_keyboard()
        if attachment:
            post["attachment"] = attachment
        self.vk_session.method("messages.send", post)

    def get_url(self, id, id_message):
        url = "None"
        message = self.vk_session.method("messages.getById", {"photos": id, "message_ids": id_message})
        max_size = 0
        for items in message.get("items"):
            attachments_list = items.get("attachments")
            for attachments in attachments_list:
                sizes_list = attachments.get("photo").get("sizes")
                for size in sizes_list:
                    if size.get("height") + size.get("width") > max_size:
                        max_size = size.get("height") + size.get("width")
                        url = size.get("url")
        return url

    def listen(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.app.handle_message(event)
