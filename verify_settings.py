import toml

def verify_settings():
    """Checks the settings.toml file for required values and provides feedback."""
    try:
        settings = toml.load("settings.toml")
    except toml.TomlDecodeError as e:
        print(f"Ошибка: Не удалось прочитать файл settings.toml. Пожалуйста, проверьте синтаксис. Ошибка: {e}")
        return

    errors = []

    # Check Telegram settings
    if "telegram" not in settings:
        errors.append("Отсутствует раздел [telegram]")
    else:
        if "api_id" not in settings["telegram"]:
            errors.append("Отсутствует api_id в разделе [telegram]")
        if "api_hash" not in settings["telegram"]:
            errors.append("Отсутствует api_hash в разделе [telegram]")

    # Check VK settings
    if "vk" not in settings:
        errors.append("Отсутствует раздел [vk]")
    else:
        if "token" not in settings["vk"]:
            errors.append("Отсутствует token в разделе [vk]")
        if "group_id" not in settings["vk"]:
            errors.append("Отсутствует group_id в разделе [vk]")

    if not errors:
        print("\033[92mНастройки успешно проверены. Все обязательные поля заполнены.\033[0m")
    else:
        print("\033[91mОбнаружены ошибки в файле настроек (settings.toml):\033[0m")
        for error in errors:
            print(f"- {error}")

if __name__ == "__main__":
    verify_settings()
