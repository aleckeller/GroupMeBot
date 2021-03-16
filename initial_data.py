import os
import CONSTANTS


commands = {
    "hey": "say_hi_to_sender",
    "learn": "learn_response",
    "reset-phrases": "reset_phrases",
    "commands": "list_commands",
    "restrict-user": "restrict_learn_user",
    "undo-restrict": "restrict_learn_user",
    "meme": "send_meme",
    "searchpics": "search_google_pics",
    "say": "say_message",
    "get-games": "get_games_response",
    "revenge-games": "get_games_response"
}

restricted_learn_users = []

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
        ),
        "restrict-user": (
            "Description: Will restrict a user so that user cannot teach " + bot_name + " any new phrases \n"
            "Usage: " + bot_name + " restrict-user user-nickname \n"
            "ADMINS-ONLY"
        ),
        "undo-restrict": (
            "Description: Will unrestrict a user so that user can teach " + bot_name + " any new phrases \n"
            "Usage: " + bot_name + " undo-restrict user-nickname \n"
            "ADMINS-ONLY"
        ),
        "meme": (
            "Description: Will get a random meme from the subreddit that is specified. If no subreddit is specified, "
            "will use the default subreddit. \n"
            "Usage: " + bot_name + " meme \n"
            "Optional Usage: " + bot_name + " meme subreddit_you_want_to_search"
        ),
        "searchpics": (
            "Description: Will search google images with the query provided \n"
            "Usage: " + bot_name + " searchpics query_you_want_to_search"
        ),
        "say": (
            "Description: " + bot_name + " will respond with what was in the message\n"
            "Usage: " + bot_name + " say message_you_want_bot_to_say"
        ),
        "get-games": (
            "Description: " + bot_name + " will respond with games for today and odds \n"
            "Available League Options: " + str(CONSTANTS.BET_ANALYZER_LEAGUE_OPTIONS) + "\n" 
            "Usage: " + bot_name + " get-games league"
        ),
        "revenge-games": (
            "Description: Will get revenge games for today (revenge game is a game where a player is playing their old team \n"
            "within " + os.environ.get("REVENGE_GAME_YEARS_BACK") + " years) and the odds for each game \n"
            "Available League Options: " + str(CONSTANTS.BET_ANALYZER_LEAGUE_OPTIONS) + "\n" 
            "Usage: " + bot_name + " revenge-games league"
        )
    }
    return descriptions.get(phrase)