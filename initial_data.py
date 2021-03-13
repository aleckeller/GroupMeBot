data = {
    "hey": "say_hi_to_sender",
    "learn": "learn_response",
    "reset-phrases": "reset_phrases",
    "commands": "list_commands"
}

def get_description(phrase, bot_name):
    descriptions = {
        "hey": (
            "Description: Will respond saying hey \n"
            "Usage: " + bot_name + " hey"
        ),
        "learn": (
            "Description: Will teach " + bot_name + " a phrase and respond when that phrase is used \n"
            "Usage: " + bot_name + " learn (what is up) (nothing much, wbu)"
        ),
        "reset-phrases": (
            "Description: Will reset any phrases the sender(you) have created \n"
            "Usage: " + bot_name + " reset-phrases"
        ),
        "commands": (
            "Description: Will list the available phrases or commands " + bot_name + " will respond to \n"
            "Usage: " + bot_name + " commands"
        )
    }
    return descriptions.get(phrase)