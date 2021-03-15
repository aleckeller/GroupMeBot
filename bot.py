import os
from inspect import getmembers, isfunction
import requests
import json

import redis_helper
import responses
import CONSTANTS
import utils

bot_response_functions = getmembers(responses, isfunction)
sender = None
message = None
sender_id = None
group_id = None

def get_group_id():
    return group_id

def get_sender_name():
    return sender

def get_sender_id():
    return sender_id

def get_message():
    return message

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
    CONSTANTS.RESTRICTED_LEARN_PHRASES.append(bot_name)
    global sender, sender_id, group_id
    sender = json_body.get("name")
    sender_id = json_body.get("sender_id")
    group_id = json_body.get("group_id")
    if bot_name:
        global message
        message = json_body.get("text")
        sender_type = json_body.get("sender_type")
        if message and sender_type and sender_type == "user":
            message = message.lower()
            if is_bot_mentioned(bot_name, message):
                print(bot_name + " was mentioned. Determining response..")
                value = analyze_message(message)
                if value:
                    response_message = ""
                    is_function_name = False
                    for function_name, function in bot_response_functions:
                        if function_name == value:
                            is_function_name = True
                            print("Calling " + function_name)
                            response_message, response_picture_url = getattr(responses, function_name)()
                    if not is_function_name:
                        response_message = value
                        response_picture_url = None
                    response["message"] = response_message
                    response["picture_url"] = response_picture_url
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
        "bot_id" : bot_id
    }
    if picture_url:
        body["attachments"] = [
            {
                "type": "image",
                "url": picture_url
            }
        ]
    message_chunks = utils.split_message_by_character_limit(message, 999)
    for count, chunk in enumerate(message_chunks):
        # Remove picture url after the first iteration
        if count == 1:
            body.pop("attachments", None)
        body["text"] = chunk
        r = requests.post(url=group_base_url, json=body)
        if r.text:
            response_json = json.loads(r.text)
            meta = response_json.get("meta")
            if meta:
                if meta.get("errors"):
                    print("There was an error sending message..")
                    print(meta.get("errors"))
                else:
                    print("Message was sent!")
        else:
            print("Message was sent!")
    
        
