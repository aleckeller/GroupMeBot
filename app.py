from flask import Flask, request

import bot
from helpers import redis_helper

app = Flask(__name__)
redis_helper.initialize_data()

@app.route("/", methods=["POST"])
def index():
    json_body = request.get_json()
    response, status_code = bot.determine_response(json_body)
    message = response.get("message")
    picture_url = response.get("picture_url")
    if message:
        bot.send_message(message, picture_url)
    return response, status_code

if __name__ == '__main__':
    app.run(threaded=True, port=5000)