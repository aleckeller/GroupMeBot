import os

import bot

json_body = {
    "group_id": os.environ.get("SCHEDULER_GROUP_ID"),
    "name": os.environ.get("SCHEDULER_NAME"),
    "sender_id": os.environ.get("SCHEDULER_SENDER_ID"),
    "sender_type": os.environ.get("SCHEDULER_SENDER_TYPE"),
    "user_id": os.environ.get("SCHEDULER_USER_ID")
}

def send_morning_meme():
    print("Sending morning meme..")
    bot_name = bot.get_bot_name()
    json_body["text"] = bot_name + " meme"
    response, status_code = bot.determine_response(json_body)
    message = response.get("message")
    picture_url = response.get("picture_url")
    if message:
        bot.send_message(message, picture_url)