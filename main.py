import datetime
import json
from operator import itemgetter
import requests

from brackets import Results, PARTICIPANTS

from texting import send_text

from google_sheets import read_sheets, write_to_sheets, append_sheet

today = datetime.date.today()

list_of_participants = []

def get_round():
    rounds ={
        'first_round' : #DATES OF THIS ROUND
                        [str(datetime.date(2021, 3, 19)),
                        str(datetime.date(2021, 3, 20))],

        'round_of_32' : [str(datetime.date(2021, 3, 21)),
                        str(datetime.date(2021, 3, 22))],

        'sweet_16' : [str(datetime.date(2021, 3, 27)),
                    str(datetime.date(2021, 3, 28))],

        'elite_8': [str(datetime.date(2021, 3, 29)),
                    str(datetime.date(2021, 3, 30))],

        'final_4' : datetime.date(2021, 4, 3),

        'championship' : datetime.date(2021, 4, 5)
        }
    
    for participant in list_of_participants:
        for current_round, date in rounds.items():
            if str(today) in str(date):
                if current_round == 'first_round':
                    participant.round = f'{participant.name}!A2:A64'
                    participant.addition = 10
                    Results.round = 'Results!A2:A64'
                elif current_round == 'round_of_32':
                    participant.round = f'{participant.name}!B2:B64'
                    Results.round = 'Results!B2:A64'
                    participant.addition = 20
                elif current_round == 'sweet_16':
                    participant.round = f'{participant.name}!C2:C64'
                    Results.round = 'Results!C2:C64'
                    participant.addition = 40
                elif current_round == 'elite_8':
                    participant.round = f'{participant.name}!D2:D64'
                    Results.round = 'Results!D2:D64'
                    participant.addition = 80
                elif current_round == 'final_4':
                    participant.round = f'{participant.name}!E2:E64'
                    Results.round = 'Results!E2:E64'
                    participant.addition = 160
                elif current_round == 'championship':
                    participant.round = f'{participant.name}!F2:F64'
                    Results.round = 'Results!F2:F64'
                    participant.addition = 320


def find_winners(current_winners):
    """
    For this I used https://rapidapi.com/api-sports/api/api-basketball

    It didn't update reliably, so in the future I'd try to find a more reliable
    source for scores and update this code as needed.
    """
    url = f""

    headers = {
        'x-rapidapi-host': "",
        'x-rapidapi-key': ""
        }

    response = requests.get(url, headers=headers)

    response_json = json.loads(response.text)

    new_winners = []
    print(response_json)
    for game in response_json['response']:
        game_over = (game['status']['short'] == 'FT')
        home_score = game['scores']['home']['total']
        away_score = game['scores']['away']['total']
        home_team = game['teams']['home']['name']
        away_team = game['teams']['away']['name']
        if game_over:
            if home_score > away_score:
                if [home_team] not in current_winners:
                    new_winners.append(home_team)
            else:
                if [away_team] not in current_winners:
                    new_winners.append(away_team)

    return new_winners

def get_score():

    points, service = read_sheets('Points')
    for participant in points:
        player = participant[0]
        score = participant[1]
        for person in list_of_participants:
            if person.name == player:
                person.score += int(score)


def compare_participants_to_results(results_from_round, current_round):

    for participant in list_of_participants:
        results = participant.round
        participant_choices, service = read_sheets(results)
        for choice in participant_choices:
            for result in results_from_round:
                if choice == result:
                    participant.score += participant.addition

    for participant in list_of_participants:
        points = [[participant.score]]
        write_to_sheets(participant.points, points, service)
    
    list_of_scores = {}
    for participant in list_of_participants:
        list_of_scores[participant.name] = participant.score

    sorted_scores = {}
    for key, value in sorted(list_of_scores.items(),
                            key=itemgetter(1), reverse=True):
        sorted_scores[key] = value

    return sorted_scores

def get_results_from_round():
    results = Results.round
    print(results)
    current_winners, service = read_sheets(results)
    new_winners = find_winners(current_winners)
    update = []
    if new_winners != []:
        for winner in new_winners:
            if [winner] not in current_winners:
                update.append([winner])
        append_sheet(results, update, service)

    return update, new_winners


def send_message(sorted_scores):

    body = f'A game just ended. The current bracket standings are: {sorted_scores}'
    for participant in list_of_participants:
        if participant.number != '':
            send_text(body, participant.number)


if __name__ == "__main__":

    current_round = get_round()
    get_score()
    current_winners, new_winners = get_results_from_round()
    if new_winners != []:
        sorted_scores = compare_participants_to_results(current_winners, current_round)
        send_message(sorted_scores)