import config

def is_premium_user(user_id):
    user_id = str(user_id)
    try:
        with open(config.PREMIUM_USERS_FILE, "r") as f:
            users = f.read().splitlines()
        return user_id in users
    except FileNotFoundError:
        return False

def add_premium_user(user_id):
    user_id = str(user_id)
    with open(config.PREMIUM_USERS_FILE, "a") as f:
        f.write(f"{user_id}\n")

def remove_premium_user(user_id):
    user_id = str(user_id)
    try:
        with open(config.PREMIUM_USERS_FILE, "r") as f:
            users = f.read().splitlines()
        with open(config.PREMIUM_USERS_FILE, "w") as f:
            for user in users:
                if user != user_id:
                    f.write(f"{user}\n")
    except FileNotFoundError:
        pass

