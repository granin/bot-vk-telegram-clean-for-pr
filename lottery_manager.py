import random
import time

class LotteryManager:
    def __init__(self, vk_handler):
        self.vk = vk_handler
        self.active = False
        self.number = None
        self.prize = None
        self.last_guess = {}

    def start_lottery(self, prize, number=None):
        self.active = True
        self.prize = prize
        if number:
            self.number = number
        else:
            self.number = random.randint(1, 1000)
        self.vk.send_to_all(f"Розыгрыш начался! Приз: {self.prize}. Угадайте число от 1 до 1000.")

    def stop_lottery(self):
        self.active = False
        self.vk.send_to_all("Розыгрыш окончен.")

    def handle_guess(self, user_id, guess):
        if not self.active:
            return

        if user_id in self.last_guess and time.time() - self.last_guess[user_id] < 30 * 60:
            self.vk.send_some_msg(user_id, "Вы можете делать предположение только раз в 30 минут.")
            return

        try:
            guess = int(guess)
        except ValueError:
            self.vk.send_some_msg(user_id, "Пожалуйста, введите число.")
            return

        self.last_guess[user_id] = time.time()

        if guess == self.number:
            self.vk.send_to_all(f"Поздравляем! Пользователь [id{user_id}|{user_id}] угадал число {self.number} и выиграл {self.prize}!")
            self.stop_lottery()
        elif guess < self.number:
            self.vk.send_some_msg(user_id, "Больше.")
        else:
            self.vk.send_some_msg(user_id, "Меньше.")
