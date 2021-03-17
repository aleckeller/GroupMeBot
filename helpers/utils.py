import requests
import os
import random

def download_image_from_url(url):
    request = requests.get(url)
    file_extension = get_file_extension(url)
    temp_picture_path = os.environ.get("TEMP_PICTURE_PATH")
    file_path = temp_picture_path + "picture." + file_extension
    with open(file_path, 'wb') as f:
        f.write(request.content)
    return file_path

def get_file_extension(path):
    return path.rpartition(".")[-1]

def split_message_by_character_limit(message, limit):
    chunks = [message[i:i+limit] for i in range(0, len(message), limit)]
    return chunks

def delete_file(file_path):
    if os.path.exists(file_path):
          os.remove(file_path)

def delete_files_in_directory(directory_path):
    filelist = [ f for f in os.listdir(directory_path)]
    for f in filelist:
        os.remove(os.path.join(directory_path, f))

def clean_message(message, bot_name, command):
    replace_list = [bot_name, command]
    for cur_word in replace_list:
            message = message.replace(cur_word, '')
    return message

def get_random_response(responses):
    responses = responses.split(",")
    return random.choice(responses).strip()

def check_if_positive(number):
    if type(number) == str:
        if isfloat(number):
            number = float(number)
        else:
            number = int(number)
    string = str(number)
    if number > 0:
        string = "+" + string
    return string

def isfloat(x):
    try:
        a = float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True
