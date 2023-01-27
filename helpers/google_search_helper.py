from google_images_search import GoogleImagesSearch
import os
import random
from helpers import utils

gis = GoogleImagesSearch(os.environ.get("GOOGLE_API_KEY"), os.environ.get("GOOGLE_PROJECT"))

def search_image(query):
    _search_params = {
        "q": query,
        "num": 10,
        "fileType": "jpg",
    }
    gis.search(search_params=_search_params)
    if len(gis.results()) > 0:
        random_index = random.randint(0, len(gis.results()) - 1)
        image = gis.results()[random_index]
        google_image_name = image.url.split("/")[-1]
        google_image_path = os.environ.get("TEMP_PICTURE_PATH") + google_image_name
        image.download(path_to_dir=os.environ.get("TEMP_PICTURE_PATH"))
    else:
        google_image_path = None
    return google_image_path