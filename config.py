import toml
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# Load settings from the TOML file
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(current_dir, "settings.toml")
settings = toml.load(settings_path)

# Telegram settings
telegram_settings = settings.get("telegram", {})
chat_name = telegram_settings.get("chat_name")
my_name = telegram_settings.get("my_name")
api_id = telegram_settings.get("api_id")
api_hash = telegram_settings.get("api_hash")

# VK settings
vk_settings = settings.get("vk", {})
token = vk_settings.get("token")
group_id = vk_settings.get("group_id")
admins_list = vk_settings.get("admins_list", [])

# Path settings
path_settings = settings.get("paths", {})
directory_input = path_settings.get("directory_input")
directory_output = path_settings.get("directory_output")
PREMIUM_USERS_FILE = path_settings.get("PREMIUM_USERS_FILE")
driver_path = path_settings.get("driver_path")

# Message settings
message_settings = settings.get("messages", {})
error = message_settings.get("error")
face_not_found = message_settings.get("face_not_found")
not_recognized = message_settings.get("not_recognized")
send_photo = message_settings.get("send_photo")
select_action = message_settings.get("select_action")
request_ok = message_settings.get("request_ok")
not_subscribed = message_settings.get("not_subscribed")
set_level = message_settings.get("set_level")
set_pay = message_settings.get("set_pay")
set_race = message_settings.get("set_race")
set_strength = message_settings.get("set_strength")
set_sex = message_settings.get("set_sex")
buy_advanced_level_text = message_settings.get("buy_advanced_level_text")
contact_clone_text = message_settings.get("contact_clone_text")
accept_response_text = message_settings.get("accept_response_text")
how_get_advance_level_text = message_settings.get("how_get_advance_level_text")

# Command settings
command_settings = settings.get("commands", {})
pattern_admin_add_premium = command_settings.get("pattern_admin_add_premium")
pattern_user_help = command_settings.get("pattern_user_help")

# Choice settings
choice_settings = settings.get("choices", {})
choice_list = choice_settings.get("choice_list", [])
race_list = choice_settings.get("race_list", [])
race_list_rus = choice_settings.get("race_list_rus", [])
strength_list = choice_settings.get("strength_list", [])
strength_list_rus = choice_settings.get("strength_list_rus", [])
level_find_clone_list = choice_settings.get("level_find_clone_list", [])
buy_methods_list = choice_settings.get("buy_methods_list", [])
sex_list = choice_settings.get("sex_list", [])

# Keyboard settings
keyboard_settings = settings.get("keyboard", {})
key_color_1 = keyboard_settings.get("key_color_1")

# Other settings
other_settings = settings.get("other", {})
time_clean = other_settings.get("time_clean")


"""Получить клавиатуру с одной кнопкой отмены"""
def get_keyboard_cancel():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(label="Отмена", color="negative")
    return keyboard


"""Получить клавиатуру для выбора действия"""
def get_keyboard_choice():
    keyboard = VkKeyboard(one_time=True)
    for i in choice_list:
        keyboard.add_button(label=i, color=key_color_1)
    return keyboard


"""Получить клавиатуру для выбора расы"""
def get_keyboard_race():
    keyboard = VkKeyboard(one_time=True)
    for i in race_list_rus:
        keyboard.add_button(label=i, color=key_color_1)
    keyboard.add_line()
    keyboard.add_button(label="Отмена", color="negative")
    return keyboard


"""Получить клавиатуру для выбора силы расы"""
def get_keyboard_strength():
    keyboard = VkKeyboard(one_time=True)
    for i in strength_list_rus:
        keyboard.add_button(label=i, color=key_color_1)
    keyboard.add_line()
    keyboard.add_button(label="Отмена", color="negative")
    return keyboard


"""Получить клавиатуру для выбора уровн запроса"""
def get_keyboard_level():
    keyboard = VkKeyboard(one_time=True)
    for i in level_find_clone_list:
        keyboard.add_button(label=i, color=key_color_1)
    keyboard.add_line()
    keyboard.add_button(label="Отмена", color="negative")
    return keyboard


"""Получить клавиатуру для оплаты"""
def get_keyboard_pay():
    keyboard = VkKeyboard(one_time=True)
    g_id = 209170407
    hash = "action=pay-to-group&amount=1&group_id="+str(g_id)+"."
    keyboard.add_vkpay_button(hash=hash, payload={"type": "canel_payment"})
    keyboard.add_line()
    keyboard.add_button(label="Отмена", color="negative")
    return keyboard


"""Получить клавиатуру для выбора пола"""
def get_keyboard_sex():
    keyboard = VkKeyboard(one_time=True)
    for i in sex_list:
        keyboard.add_button(label=i, color=key_color_1)
    keyboard.add_line()
    keyboard.add_button(label="Отмена", color="negative")
    return keyboard


"""Получить клавиатуру для выбора связи с двойником"""
def get_keyboard_contact():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(label=contact_clone_text, color=key_color_1)
    keyboard.add_line()
    keyboard.add_button(label="Отмена", color="negative")
    return keyboard


"""Получить клавиатуру для выбора связи с двойником и покупки полного доступа"""
def get_keyboard_contact_and_level():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(label=contact_clone_text, color=key_color_1)
    keyboard.add_line()
    keyboard.add_button(label=buy_advanced_level_text, color=key_color_1)
    keyboard.add_line()
    keyboard.add_button(label="Закрыть", color="negative")
    return keyboard


"""Получить клавиатуру для получения полного доступа"""
def get_keyboard_buy_advance_level():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_openlink_button(link="http://example.com/donut", label=buy_methods_list[0])
    keyboard.add_line()
    keyboard.add_button(label=buy_methods_list[1], color=key_color_1)
    keyboard.add_line()
    keyboard.add_button(label="Отмена", color="negative")
    return keyboard
