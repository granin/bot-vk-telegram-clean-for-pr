import re
from datetime import datetime
import config
from lottery_manager import LotteryManager
from user_manager import is_premium_user, add_premium_user, remove_premium_user
from queue_manager import QueueManager
from telegram_handler import TelegramHandler
from vk_handler import VkHandler
from worker import Worker
from utils import cut_photo, cut_photo_2, clear_mem

class App:
    def __init__(self):
        self.client_requests = {}
        self.vk = VkHandler(self)
        self.telegram = TelegramHandler()
        self.queue = QueueManager()
        self.lottery = LotteryManager(self.vk)
        self.queue.start()
        self.vk.listen()

    def handle_message(self, event):
        user_id = event.user_id
        msg_text = event.text
        msg_id = event.message_id

        if not self.vk.session_api.groups.isMember(group_id=config.group_id, user_id=user_id):
            self.vk.send_message(user_id, config.not_subscribed)
            return

        if msg_text.startswith("/"):
            self.handle_command(user_id, msg_text)
            return

        if event.attachments.get("attach1_type") == 'photo':
            self.handle_photo(user_id, event)
            return

        if msg_text.lower() == "лотерея":
            self.lottery.start_lottery()
            return

        if msg_text.isdigit():
            self.lottery.handle_guess(user_id, int(msg_text))
            return

        if user_id in self.client_requests:
            self.handle_client_request(user_id, msg_text)
        else:
            self.vk.send_message(user_id, config.send_photo)

    def handle_command(self, user_id, command):
        if user_id not in config.admins_list:
            return

        if command.startswith(config.pattern_admin_add_premium):
            try:
                add_user_id = command.split(" ")[1]
                add_premium_user(add_user_id)
                self.vk.send_message(user_id, f"Пользователь {add_user_id} получил премиум доступ.")
                self.vk.send_message(add_user_id, "Вам предоставлен премиум доступ.")
            except IndexError:
                self.vk.send_message(user_id, "Неверный формат команды.")
        elif command.startswith("/start_lottery"):
            try:
                prize = command.split(" ")[1]
                number = int(command.split(" ")[2]) if len(command.split(" ")) > 2 else None
                self.lottery.start_lottery(prize, number)
            except (IndexError, ValueError):
                self.vk.send_message(user_id, "Неверный формат команды.")
        elif command == "/stop_lottery":
            self.lottery.stop_lottery()

    def handle_photo(self, user_id, event):
        photo_url = self.vk.get_url(event.attachments.get("attach1"), event.message_id)
        if photo_url == "multiple_faces" or photo_url == "no_face":
            self.vk.send_message(user_id, config.face_not_found)
            return

        self.client_requests[user_id] = {
            "stage": "choice",
            "photo_url": photo_url,
        }
        self.vk.send_message(user_id, config.select_action, keyboard=config.get_keyboard_choice())

    def handle_client_request(self, user_id, msg_text):
        request = self.client_requests[user_id]

        if msg_text == "Отмена":
            del self.client_requests[user_id]
            self.vk.send_message(user_id, "Действие отменено.")
            return

        if request["stage"] == "choice":
            if msg_text in config.choice_list:
                request["choice"] = msg_text
                if msg_text == "Найти двойника":
                    request["stage"] = "sex"
                    self.vk.send_message(user_id, config.set_sex, keyboard=config.get_keyboard_sex())
                elif msg_text == "Смена расы":
                    if len(self.queue.queue) >= 100:
                        self.vk.send_message(user_id, "Превышен дневной лимит обработки.")
                        return
                    request["stage"] = "race"
                    self.vk.send_message(user_id, config.set_race, keyboard=config.get_keyboard_race())
                elif msg_text == "Другое":
                    self.vk.send_message(user_id, "Этот раздел в разработке.")
                elif msg_text == "Обратная связь":
                    request["stage"] = "feedback"
                    self.vk.send_message(user_id, "Введите ваше сообщение:")
            else:
                self.vk.send_message(user_id, config.not_recognized)

        elif request["stage"] == "sex":
            sex = None
            if msg_text == "Мужской":
                sex = "m"
            elif msg_text == "Женский":
                sex = "f"

            if sex:
                premium = is_premium_user(user_id)
                if premium:
                    remove_premium_user(user_id)
                w = Worker(self.vk.session_api, user_id, request["photo_url"], sex, premium=premium)
                self.queue.add_to_queue(w)
                self.vk.send_message(user_id, f"Ваша заявка принята. Ваш номер в очереди: {len(self.queue.queue)}")
                del self.client_requests[user_id]
            else:
                self.vk.send_message(user_id, config.not_recognized)

        elif request["stage"] == "race":
            if msg_text in config.race_list_rus:
                request["race"] = config.race_list[config.race_list_rus.index(msg_text)]
                request["stage"] = "strength"
                self.vk.send_message(user_id, config.set_strength, keyboard=config.get_keyboard_strength())
            else:
                self.vk.send_message(user_id, config.not_recognized)

        elif request["stage"] == "strength":
            if msg_text in config.strength_list_rus:
                strength = config.strength_list[config.strength_list_rus.index(msg_text)]
                # TODO: Implement telegram photo processing
                self.vk.send_message(user_id, "Этот раздел в разработке.")
                del self.client_requests[user_id]
            else:
                self.vk.send_message(user_id, config.not_recognized)

        elif request["stage"] == "feedback":
            self.telegram.send_message(f"Сообщение от пользователя {user_id}: {msg_text}")
            self.vk.send_message(user_id, "Ваше сообщение отправлено администратору.")
            del self.client_requests[user_id]

if __name__ == "__main__":
    App()
