import praw
import os

from helpers import utils
import CONSTANTS

reddit_client = praw.Reddit(client_id=os.environ.get("REDDIT_CLIENT_ID"),
                            client_secret=os.environ.get("REDDIT_CLIENT_SECRET"), 
                            user_agent=os.environ.get("REDDIT_USER_AGENT"))

def get_random_meme_url(subreddit_name):
    subreddit = reddit_client.subreddit(subreddit_name)
    meme_url = None
    meme_url_found = False
    while not meme_url_found:
        meme = subreddit.random()
        if meme.__getattr__("url"):
            file_extension = utils.get_file_extension(meme.url)
            if file_extension in CONSTANTS.ACCEPTED_MEME_FILE_EXTENSIONS:
                meme_url_found = True
                meme_url = meme.url
    return meme_url