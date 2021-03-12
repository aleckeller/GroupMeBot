import re
import os

import bot
import redis_helper

def say_hi_to_sender():
    sender = bot.get_sender_name()
    message = ""
    if sender:
        message = "hi " + sender
    else:
        message = "hi"
    return message

def learn_response():
    response = None
    bot_name = bot.get_bot_name()
    sender = bot.get_sender_name()
    message = bot.get_message()
    sender_learn_amount_key = sender + "_learn_amount"
    if message:
        parsed_data_between_parentheses = re.findall("\((.*?)\)", message)
        if len(parsed_data_between_parentheses) == 2:
            phrase = parsed_data_between_parentheses[0]
            bot_response = parsed_data_between_parentheses[1]
            learn_limit = int(os.environ.get("LEARN_LIMIT")) or 2
            sender_learn_amount = redis_helper.get_value(sender_learn_amount_key)
            if sender_learn_amount:
                sender_learn_amount = int(sender_learn_amount)
            else:
                sender_learn_amount = 0
                success = redis_helper.set_key_value(sender_learn_amount_key, sender_learn_amount)
                if not success:
                    print("There was an error setting the sender learn amount value in redis")
            if sender_learn_amount <= learn_limit:
                success = redis_helper.set_key_value(phrase, bot_response)
                if success:
                    response = (
                        bot_name + " successfully learned phrase "
                        "(" + phrase + ") with response (" + bot_response + ")"
                    )
                else:
                    response = (
                        "There was an error learning phrase "
                        "(" + phrase + ") with response (" + bot_response + ") :/"
                    )

        else:
            response = (
                "Learn message has incorrect structure. "
                "Please use the following format -> \n" +
                bot_name + " learn (phrase) (response)"
                ""
            )

    return response
