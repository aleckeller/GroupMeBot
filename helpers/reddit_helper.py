import praw
import os
import random

from helpers import utils
import CONSTANTS

reddit_client = praw.Reddit(client_id=os.environ.get("REDDIT_CLIENT_ID"),
                            client_secret=os.environ.get("REDDIT_CLIENT_SECRET"), 
                            user_agent=os.environ.get("REDDIT_USER_AGENT"))

def get_random_meme_url(subreddit_name):
    try:
        subreddit = reddit_client.subreddit(subreddit_name)
    except:
        print("Error connecting to reddit..")
        subreddit = None
    meme_url = None
    if subreddit:
        meme_url_found = False
        max_retries = 10
        retries = 1
        while not meme_url_found and retries < max_retries:
            try:
                rising_submissions = subreddit.top(limit=10, time_filter="month")
            except:
                print("Error connecting to reddit..")
                rising_submissions = []
            meme = None
            # Convert ListingGenerator to list
            rising_submissions_list = []
            for submission in rising_submissions:
                rising_submissions_list.append(submission)
            meme = random.choice(rising_submissions_list)
            if meme and meme.__getattr__("url"):
                file_extension = utils.get_file_extension(meme.url)
                if file_extension in CONSTANTS.ACCEPTED_MEME_FILE_EXTENSIONS:
                    meme_url_found = True
                    meme_url = meme.url
            retries = retries + 1
    return meme_url