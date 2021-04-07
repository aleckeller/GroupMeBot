import requests
import os
import json
import time

import bot
from helpers import utils

sports_bet_analyzer_base_url = os.environ.get("SPORTS_BET_ANALYZER_URL")
revenge_game_years_back = int(os.environ.get("REVENGE_GAME_YEARS_BACK"))

def get_games(league, date, is_revenge_games, get_odds):
    body = {
        "include_odds": get_odds,
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
    bot.send_message("Processing request for the sports bet analyzer..")
    while not request_finished:
        r = requests.get(url=request_url)
        if r.status_code != 202:
            response = json.loads(r.text)
            request_finished = True
        else:
            time.sleep(3)
    return response

def format_games(games, is_revenge_games, is_get_odds, command, league):
    response = ""
    for game in games:
        away_team = game["away_team"]["name"]
        home_team = game["home_team"]["name"]
        odds = None
        if game.get("odds"):
            odds = get_odds(game["odds"])
        else:
            odds = "Odds currently not available (in-progress game)"
        response = response + (
            f"{away_team} vs. {home_team} \n\n"
        )
        if is_revenge_games:
            revenge_game_players = get_revenge_players_string(game["revenge_game_players"])
            response = response + (
                f"Revenge Game Players: \n"
                f"{revenge_game_players}"
                "\n"
            )
        previous_head_to_heads = get_previous_head_to_heads(game)
        response = response + (
            "Previous Head to Heads: \n"
            f"{previous_head_to_heads} \n"
        )
        if is_get_odds:
            response = response + (
                f"{odds} \n"
                "------------------------------------"
                "\n"
            )
        else:
            response = response + (
                "------------------------------------"
                "\n"
            )
    if not is_get_odds:
        response = response + (
            f"(Remember to run the following command if you want odds: {bot.get_bot_name()} "
            f"{command} {league} odds"
            "\n"
        )
    response = response[:-1]
    return response

def get_revenge_players_string(revenge_game_players):
    the_string = ""
    for player in revenge_game_players:
        years_string = ""
        for year in player["previous_team_years"]:
            years_string = years_string + str(year) + " " 
        the_string = (
            the_string + player["name"] + "(" + player["current_team_name"] + "): "
            "previously played on " + player["previous_team_name"] + " for the following years -> " +
            years_string + "\n" + "-------" + "\n"
        )
    the_string = the_string[:-8]
    return the_string

def get_odds(odds):
    odds_data = odds.get("odds")
    teams = odds.get("teams")
    odds_string = ""
    teams_with_odds = []
    index = 0
    for index in range(2):
        team = {}
        for sportsbook, markets in odds_data.items():
            totals_position = markets["totals"]["position"]
            if totals_position[0] == "over":
                over_index = 0
                under_index = 1
            else:
                over_index = 1
                under_index = 0
            team[sportsbook] = {
                "h2h": markets["h2h"][index],
                "spreads": {
                    "odds": markets["spreads"]["odds"][index],
                    "points": markets["spreads"]["points"][index]
                },
                "totals": {
                    "over": {
                        "odds": markets["totals"]["odds"][over_index],
                        "points": markets["totals"]["points"][over_index]
                    },
                    "under": {
                        "odds": markets["totals"]["odds"][under_index],
                        "points": markets["totals"]["points"][under_index]
                    } 
                }
            }
        teams_with_odds.append(team)
    for index, team_odds in enumerate(teams_with_odds):
        team_name = teams[index]
        odds_string = odds_string + f"{team_name} odds: \n"
        for sportsbook, markets in team_odds.items():
            h2h = utils.check_if_positive(markets["h2h"])
            spread_odds = utils.check_if_positive(markets["spreads"]["odds"])
            spread_points = utils.check_if_positive(markets["spreads"]["points"])
            totals_over_odds = utils.check_if_positive(markets["totals"]["over"]["odds"])
            totals_over_points = markets["totals"]["over"]["points"]
            totals_under_odds = utils.check_if_positive(markets["totals"]["under"]["odds"])
            totals_under_points = markets["totals"]["under"]["points"]
            odds_string = odds_string + (
                f"  {sportsbook} -> \n"
                f"    Moneyline: {h2h} odds \n"
                f"    Spread: {spread_points} points at {spread_odds} odds \n"
                f"    O: {totals_over_points} points at {totals_over_odds} odds \n"
                f"    U: {totals_under_points} points at {totals_under_odds} odds \n"
            )
        odds_string = odds_string + "\n"
    return odds_string

def get_previous_head_to_heads(game_data):
    previous_head_to_heads_string = ""
    for game in game_data["previous_head_to_heads"]:
        if game["winner"] == game_data["home_team"]["abbreviation"]:
            winner = game_data["home_team"]["name"]
        else:
            winner = game_data["away_team"]["name"]
        previous_head_to_heads_string = previous_head_to_heads_string + (
            f"Winner: {winner} \n"
            f"Score: {game['score']} \n"
            f"Date: {game['date']}\n"
            "------- \n"
        )
    previous_head_to_heads_string = previous_head_to_heads_string[:-9]
    return previous_head_to_heads_string
    