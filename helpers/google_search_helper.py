from google_images_search import GoogleImagesSearch
import os
import random
from helpers import utils

gis = GoogleImagesSearch(os.environ.get("GOOGLE_API_KEY"), os.environ.get("GOOGLE_PROJECT"))

def search_image(query):
    google_image_name = "google_image"
    file_type = "jpg"
    _search_params = {
        "q": query,
        "num": 10,
        "fileType": file_type,
    }
    gis.search(search_params=_search_params, custom_image_name=google_image_name)
    if len(gis.results()) > 0:
        random_index = random.randint(0, len(gis.results()) - 1)
        google_image_path = os.environ.get("TEMP_PICTURE_PATH") + google_image_name + "." + file_type
        utils.delete_file(google_image_path)
        gis.results()[random_index].download(path_to_dir=os.environ.get("TEMP_PICTURE_PATH"))
    else:
        google_image_path = None
    return google_image_path