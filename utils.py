import requests
import os

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