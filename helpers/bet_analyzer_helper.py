import requests
import os
import json
import time
import bot

sports_bet_analyzer_base_url = os.environ.get("SPORTS_BET_ANALYZER_URL")
revenge_game_years_back = int(os.environ.get("REVENGE_GAME_YEARS_BACK"))

def get_games(league, date, is_revenge_games):
    body = {
        "date": date,
        "leagues": {
            league: {
               "json_logic": [] 
            }
        }
    }
    url = sports_bet_analyzer_base_url
    if is_revenge_games:
        url = url + "/revenge-games/"
        body["number_of_years_back"] = revenge_game_years_back
    else:
        url = url + "/games/"
    request_id = get_request_id(url, body)
    return get_response_from_request_id(request_id)


def get_request_id(url, body):
    request_id = None
    r = requests.post(url=url, json=body)
    if r.text:
        response_json = json.loads(r.text)
        if response_json.get("id"):
            request_id = response_json["id"]
        elif response_json.get("error"):
            print("Error getting request id -> ")
            print(response_json["error"])
    return request_id

def get_response_from_request_id(request_id):
    response = None
    request_url = sports_bet_analyzer_base_url + "/results/" + request_id
    request_finished = False
    bot.send_message("Processing request for the sports bet analyzer.. this can take a couple of minutes.")
    request_attempts = 0
    while not request_finished:
        r = requests.get(url=request_url)
        if r.status_code != 202:
            response = json.loads(r.text)
            request_finished = True
        else:
            if request_attempts > 0:
                bot.send_message("Still processing games..")
            time.sleep(30)
        request_attempts = request_attempts + 1
    return response
    