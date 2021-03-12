import os
from inspect import getmembers, isfunction
import requests

import redis_helper
import responses

bot_response_functions = getmembers(responses, isfunction)
sender = None

def get_sender_name():
    return sender

def get_bot_name():
    bot_name = os.environ.get("BOT_NAME")
    if bot_name:
        bot_name = bot_name.lower()
    return bot_name

def is_bot_mentioned(bot_name, message):
    return bot_name in message

def analyze_message(message):
    value = None
    redis_keys = redis_helper.get_keys()
    for key in redis_keys:
        key = str(key)
        if key in message:
            print("Found " + key + " in message!")
            value = redis_helper.get_value(key)
    return value

def determine_response(json_body):
    response = {}
    status_code = 200
    bot_name = get_bot_name()
    global sender
    sender = json_body.get("name")
    if bot_name:
        message = json_body.get("text")
        if message:
            message = message.lower()
            if is_bot_mentioned(bot_name, message):
                print(bot_name + " was mentioned. Determining response..")
                value = analyze_message(message)
                if value:
                    is_function_name = False
                    for function_name, function in bot_response_functions:
                        if function_name == value:
                            is_function_name = True
                            print("Calling " + function_name)
                            result = getattr(responses, function_name)()
                            response["message"] = result
                    if not is_function_name:
                        response["message"] = result
    else:
        response = {
            "error": "BOT_NAME environment variable not defined"
        }
        status_code = 500
    return response, status_code

def send_message(message, picture_url=None):
    group_base_url = os.environ.get("GROUP_BASE_URL")
    bot_id = os.environ.get("BOT_ID")
    body = {
      "bot_id" : bot_id,
      "text" : message
    }
    if picture_url:
        body["attachments"] = [
            {
                "type": "image",
                "url": picture_url
            }
        ]
    r = requests.post(url=group_base_url, json=body)
    print("Message was sent!")
    
        
