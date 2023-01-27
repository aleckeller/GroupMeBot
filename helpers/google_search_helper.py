from google_images_search import GoogleImagesSearch
import os
import random
from helpers import utils

gis = GoogleImagesSearch(os.environ.get("GOOGLE_API_KEY"), os.environ.get("GOOGLE_PROJECT"))

def search_image(query):
    file_type = "jpg"
    _search_params = {
        "q": query,
        "num": 10,
        "fileType": file_type,
    }
    gis.search(search_params=_search_params)
    if len(gis.results()) > 0:
        random_index = random.randint(0, len(gis.results()) - 1)
        gis.results()[random_index].download(path_to_dir=os.environ.get("TEMP_PICTURE_PATH"))
    else:
        google_image_path = None
    return google_image_path