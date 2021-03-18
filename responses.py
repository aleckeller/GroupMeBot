import re
import os
from datetime import datetime
import pytz

import bot
from helpers import redis_helper
import initial_data
import CONSTANTS
from helpers import groupme_helper
from helpers import reddit_helper
from helpers import utils
from helpers import google_search_helper
from helpers import bet_analyzer_helper

def say_hi_to_sender():
    sender = bot.get_sender_name()
    message = ""
    if sender:
        message = "hi " + sender
    else:
        message = "hi"
    return message, None

def learn_response():
    response = None
    bot_name = bot.get_bot_name()
    sender = bot.get_sender_name()
    sender_id = bot.get_sender_id()
    message = bot.get_message()
    group_id = bot.get_group_id()
    sender_learn_amount_key = sender_id + "_learn_amount"
    sender_learn_phrases_key = sender_id + "_learn_phrases"
    restricted_learn_users = redis_helper.get_list("restricted_learn_users")
    if sender_id not in restricted_learn_users:
        if message:
            parsed_data_between_parentheses = re.findall("\((.*?)\)", message)
            if len(parsed_data_between_parentheses) == 2:
                phrase = parsed_data_between_parentheses[0]
                bot_response = parsed_data_between_parentheses[1]
                if phrase not in CONSTANTS.RESTRICTED_LEARN_PHRASES:
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
                                description =  list_commands(short_version=True)[0]
                                groupme_helper.update_group_description(group_id, description)
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
                    response = "(" + phrase + ")" + " is a restricted phrase and " + bot_name + " cannot learn it"

            else:
                response = (
                    "Learn message has incorrect structure. "
                    "Please use the following format -> \n" +
                    bot_name + " learn (phrase) (response)"
                )
    else:
        response = (
            sender + ", you are a restricted user and cannot teach " + bot_name + " any new phrases. "
            "Contact an admin to become unrestricted."
        )

    return response, None

def reset_phrases(sender=None, sender_id=None):
    if not sender:
        sender = bot.get_sender_name()
    if not sender_id:
        sender_id = bot.get_sender_id()
    group_id = bot.get_group_id()
    sender_learn_amount_key = sender_id + "_learn_amount"
    sender_learn_phrases_key = sender_id + "_learn_phrases"
    sender_learned_phrases = redis_helper.get_list(sender_learn_phrases_key)
    for phrase in sender_learned_phrases:
        redis_helper.delete_key(phrase)
    redis_helper.delete_key(sender_learn_phrases_key)
    redis_helper.set_key_value(sender_learn_amount_key, 0)
    description =  list_commands(short_version=True)[0]
    groupme_helper.update_group_description(group_id, description)
    response = "Successfully removed all learned phrases for " + sender
    return response, None

def list_commands(short_version=False):
    bot_name = bot.get_bot_name()
    response = "Here are the current phrases " + bot_name + " will respond to if included in a message -> \n\n"
    phrases = redis_helper.get_keys()
    learn_amount_key_end = "_learn_amount"
    learn_phrases_key_end = "_learn_phrases"
    for phrase in phrases:
        if (not learn_amount_key_end in phrase) and (not learn_phrases_key_end in phrase):
            if not short_version:
                description = initial_data.get_description(phrase, bot_name)
                if description:
                    response = response + "Phrase: " +  phrase + "\n" + description + "\n" + "-------------" + "\n"
                else:
                    response = response + "Phrase: " + phrase + " (custom phrase) " + "\n" + "-------------" + "\n"
            else:
                response = response + "(" + phrase + ") "
    return response, None

def restrict_learn_user():
    response = None
    bot_name = bot.get_bot_name()
    message = bot.get_message()
    sender = bot.get_sender_name()
    group_id = bot.get_group_id()
    if message:
        message_split = message.split(" ")
        if len(message_split) >= 3:
            action = message_split[1]
            restricted_user_nickname = utils.clean_message(message, bot_name, action).strip()
            sender_id = bot.get_sender_id()
            admin_user_ids = os.environ.get("ADMIN_USER_IDS")
            admin_user_ids = admin_user_ids.split(",")
            if sender_id in admin_user_ids:
                restricted_user_id = groupme_helper.get_user_id_from_group(group_id, restricted_user_nickname)
                if restricted_user_id:
                    if action == "restrict-user":
                        redis_helper.append_to_list("restricted_learn_users", restricted_user_id)
                        reset_phrases(restricted_user_nickname, restricted_user_id)
                        response = "Restricted the following user: " + restricted_user_nickname
                    elif action == "undo-restrict":
                        redis_helper.remove_from_list("restricted_learn_users", restricted_user_id)
                        response = "Unrestricted the following user: " + restricted_user_nickname
                    else:
                        response = "Unknown action"
                else:
                    response = restricted_user_nickname + " is not a user in this group"
            else:
                response = sender + " is not an admin and cannot restrict users"
        else:
            response = (
                "Restrict/undo users has incorrect structure "
            )

    return response, None

def send_meme():
    message = bot.get_message()
    message_split = message.split(" ")
    if len(message_split) == 3:
        subreddit_name = message_split[2]
    else:
        subreddit_name = os.environ.get("MEME_SUBREDDIT")
    groupme_picture = None
    groupme_picture_found = False
    get_meme_retries = int(os.environ.get("GET_MEME_RETRIES"))
    for i in range(1, get_meme_retries + 1):
        print("On try " + str(i) + " trying to get a meme..")
        meme_url = reddit_helper.get_random_meme_url(subreddit_name)
        if meme_url:
            file_path = utils.download_image_from_url(meme_url)
            groupme_picture = groupme_helper.upload_picture(file_path)
            if groupme_picture:
                groupme_picture_found = True
                break
    if groupme_picture_found:
        response_message = os.environ.get("MEME_RESPONSE_MESSAGE") + " (subreddit -> " + subreddit_name + ")"
        picture_url = groupme_picture.get("picture_url")
    else:
        response_message = "There was an error trying to get a meme.. Please try again"
        picture_url = None
    return response_message, picture_url

def search_google_pics():
    bot_name = bot.get_bot_name()
    message = bot.get_message()
    message_split = message.split(" ")
    picture_url = None
    if len(message_split) >= 3:
        command = message_split[1]
        clean_message = utils.clean_message(message, bot_name, command)
        image_path = google_search_helper.search_image(clean_message)
        if image_path:
            groupme_picture = groupme_helper.upload_picture(image_path)
            response_message = "Results for the query -> " + clean_message.strip()
            picture_url = groupme_picture.get("picture_url")
        else:
            response_message = "Sorry, could not find any results for " + clean_message.strip()
    else:
        response_message = "No query provided to search with.."
    return response_message, picture_url

def say_message():
    bot_name = bot.get_bot_name()
    message = bot.get_message()
    message_split = message.split(" ")
    picture_url = None
    if len(message_split) >= 3:
        command = message_split[1]
        response_message = utils.clean_message(message, bot_name, command).strip()
    else:
        response_message = "Nothing to say.."
    return response_message, picture_url

def get_games_response():
    bot_name = bot.get_bot_name()
    message = bot.get_message()
    message_split = message.split(" ")
    picture_url = None
    if len(message_split) >= 3:
        command = message_split[1]
        league = message_split[2]
        if league in CONSTANTS.BET_ANALYZER_LEAGUE_OPTIONS:
            utc_now = pytz.utc.localize(datetime.utcnow())
            now = utc_now.astimezone(pytz.timezone(os.environ.get("TIMEZONE"))).strftime("%m-%d-%Y")
            is_revenge_games = command == "revenge-games"
            response = bet_analyzer_helper.get_games(league, now, is_revenge_games)
            if not response.get("error"):
                data = response["data"]
                games = data.get(league)
                if games and len(games) > 0:
                    if is_revenge_games:
                        response_message = (
                            f"Revenge Games for {now}: \n" +
                            bet_analyzer_helper.format_games(games, True)
                        )
                    else:
                        response_message = (
                            f"Games for {now}: \n" +
                            bet_analyzer_helper.format_games(games, False)
                        )
                else:
                    response_message = "There are no games today in the " + league 
            else:
                response_message = (
                    "Error getting games -> \n" + 
                    response["error"]
                )

        else:
            response_message = "League needs to be one of the following -> " + str(CONSTANTS.BET_ANALYZER_LEAGUE_OPTIONS)

    else:
        response_message = (
            "Revenge-games or get-games has incorrect structure. "
            "Please use the following format -> " 
            "(note that the following league options are available " + str(CONSTANTS.BET_ANALYZER_LEAGUE_OPTIONS) + " \n)" +
            bot_name + " (revenge-games or get-games) league_you_want_games_for"
        )
    return response_message, picture_url

