import re
import os

import bot
import redis_helper
import initial_data

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
    sender_id = bot.get_sender_id()
    message = bot.get_message()
    sender_learn_amount_key = sender_id + "_learn_amount"
    sender_learn_phrases_key = sender_id + "_learn_phrases"
    if message:
        parsed_data_between_parentheses = re.findall("\((.*?)\)", message)
        if len(parsed_data_between_parentheses) == 2:
            phrase = parsed_data_between_parentheses[0]
            bot_response = parsed_data_between_parentheses[1]
            learn_limit = int(os.environ.get("LEARN_LIMIT")) or 2
            sender_learn_amount = redis_helper.get_value(sender_learn_amount_key)
            sender_learned_phrases = redis_helper.get_list(sender_learn_phrases_key)
            if sender_learn_amount:
                sender_learn_amount = int(sender_learn_amount)
            else:
                sender_learn_amount = 0
            if sender_learn_amount < learn_limit:
                if not redis_helper.get_value(phrase):
                    success = redis_helper.set_key_value(phrase, bot_response)
                    if success:
                        redis_helper.set_key_value(sender_learn_amount_key, sender_learn_amount + 1)
                        redis_helper.append_to_list(sender_learn_phrases_key, phrase)
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
                    sender_learned_phrases_string = ""
                    if sender_learned_phrases:
                        for sender_learned_phrase in sender_learned_phrases:
                            sender_learned_phrases_string = sender_learned_phrases_string + "(" + sender_learned_phrase + ") "
                    response = (
                        bot_name + " already knows the phrase (" + phrase + "). "
                        "If you own this phrase, you can reset the learned phrases "
                        "you have set. Here are the learned phrases you have set -> " +
                        sender_learned_phrases_string
                    )
            else:
                response = (
                    sender + ", you have reached your limit of " + str(learn_limit) + 
                    " learned phrases. Please send the following message if you wish "
                    "to reset your learned phrases -> \n" +
                    bot_name + " reset-phrases"
                )

        else:
            response = (
                "Learn message has incorrect structure. "
                "Please use the following format -> \n" +
                bot_name + " learn (phrase) (response)"
                ""
            )

    return response

def reset_phrases():
    sender = bot.get_sender_name()
    sender_id = bot.get_sender_id()
    sender_learn_amount_key = sender_id + "_learn_amount"
    sender_learn_phrases_key = sender_id + "_learn_phrases"
    sender_learned_phrases = redis_helper.get_list(sender_learn_phrases_key)
    for phrase in sender_learned_phrases:
        redis_helper.delete_key(phrase)
    redis_helper.delete_key(sender_learn_phrases_key)
    redis_helper.set_key_value(sender_learn_amount_key, 0)
    response = "Successfully removed all learned phrases for " + sender
    return response

def list_commands():
    bot_name = bot.get_bot_name()
    response = "Here are the current phrases " + bot_name + " will respond to -> \n\n"
    phrases = redis_helper.get_keys()
    learn_amount_key_end = "_learn_amount"
    learn_phrases_key_end = "_learn_phrases"
    for phrase in phrases:
        if (not learn_amount_key_end in phrase) and (not learn_phrases_key_end in phrase):
            description = initial_data.get_description(phrase, bot_name)
            if description:
                response = response + "Phrase: " +  phrase + "\n" + description + "\n" + "-------------" + "\n"
            else:
                response = response + "Phrase: " + phrase + " (custom phrase) " + "\n" + "-------------" + "\n"
    return response
