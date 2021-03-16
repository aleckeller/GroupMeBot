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

def format_revenge_games(revenge_games):
    response = ""
    for game in revenge_games:
        away_team = game["away_team"]["name"]
        home_team = game["home_team"]["name"]
        revenge_game_players = get_revenge_players_string(game["revenge_game_players"])
        odds = get_odds(game["odds"])
        
        response = response + (
            f"{away_team} vs. {home_team} \n\n"
            f"{odds} \n"
            f"Revenge Game Players: {revenge_game_players}"
            "\n"
            "------------------------------------"
            "\n"
        )
    response = response[:-1]
    return response

def get_revenge_players_string(revenge_game_players):
    the_string = ""
    for player in revenge_game_players:
        the_string = the_string + player["name"] + ", "
    the_string = the_string.strip()[:-1]
    return the_string

def get_odds(odds):
    odds_data = odds["odds"]
    teams = odds["teams"]
    teams_with_odds = []
    index = 0
    for index in range(2):
        team = {}
        for sportsbook, markets in odds_data.items():
            team[sportsbook] = {
                "h2h": markets["h2h"][index],
                "spreads": {
                    "odds": markets["spreads"]["odds"][index],
                    "points": markets["spreads"]["points"][index]
                },
                "totals": {
                    "odds": markets["totals"]["odds"][index],
                    "points": markets["totals"]["points"][index]
                }
            }
        teams_with_odds.append(team)
    odds_string = ""
    for index, team_odds in enumerate(teams_with_odds):
        team_name = teams[index]
        odds_string = odds_string + f"{team_name} odds: \n"
        for sportsbook, markets in team_odds.items():
            h2h = markets["h2h"]
            spread_odds = markets["spreads"]["odds"]
            spread_points = markets["spreads"]["points"]
            totals_odds = markets["totals"]["odds"]
            totals_points = markets["totals"]["points"]
            odds_string = odds_string + (
                f"  {sportsbook} -> \n"
                f"    Moneyline: {h2h} odds \n"
                f"    Spread: {spread_points} points at {spread_odds} odds \n"
                f"    O/U: {totals_points} points at {totals_odds} odds \n"
            )
        odds_string = odds_string + "\n"
    return odds_string
