from datetime import datetime
import json

with open("match_list.json", mode="r", encoding="utf-8") as read_file:
    data = json.load(read_file)

with open("alt_names.json", mode="r", encoding="utf-8") as read_file:
    alt_names = json.load(read_file)

with open("teams_geo_info.json", mode="r", encoding="utf-8") as read_file:
    teams_geo_info = json.load(read_file)

def resolve_club_name(club_name):
    return alt_names.get(club_name, club_name)

date_format = '%d/%m/%Y'
winners_count = {}
leaders_count = {}
most_wins = 0
currentLeader = ""
#
# for match in data:
#     if 'Winner' in match and match['Winner'] != 'Tie':
#         if match['Winner'] in alt_names:
#             name = alt_names[match['Winner']]
#         else:
#             name = match['Winner']
#
#         if name not in winners_count:
#             winners_count[name] = 1
#         else:
#             winners_count[name] += 1


def winners_sorted(winners_count):
    sorted_list_of_tuples = sorted(
        winners_count.items(),
        key=lambda item: item[1],
        reverse=True
    )

    sorted_winners_count = dict(sorted_list_of_tuples)

    return sorted_winners_count


# winners_count = winners_sorted(winners_count)

def add_to_counter(key, _dict):
    if key in _dict:
        _dict[key] += 1
    else:
        _dict[key] = 1

def display_ranking(_dict):
    place = 1
    last_count = None
    for i, value in enumerate(_dict):
        if _dict[value] != last_count:
            place = i + 1
            last_count = _dict[value]
        print(str(place) + ". " + value + " - " + str(_dict[value]))

def countries_matchups():
    countries_matchup_dict = {}

    for match in data:
        home = resolve_club_name(match['Home'])
        away = resolve_club_name(match['Away'])

        home_country = teams_geo_info[home]['country']
        away_country = teams_geo_info[away]['country']

        if home_country == away_country:
            continue

        matchup = ' - '.join(sorted([home_country, away_country]))

        if matchup == 'Germany - Spain':
            print(home + " - " + away)

        add_to_counter(matchup, countries_matchup_dict)

    countries_matchup_dict = winners_sorted(countries_matchup_dict)

    display_ranking(countries_matchup_dict)

# countries_matchups()

def most_clubs_with_no_title_countries():
    clubs = list(teams_geo_info.keys())
    clubs.remove('tbc')

    for match in data:
        winner = resolve_club_name(match['Winner'])
        if winner in clubs:
            clubs.remove(winner)

    countries_count = {}
    for club in clubs:
        if teams_geo_info[club]['country'] == 'France':
            print(club)
        add_to_counter(teams_geo_info[club]['country'], countries_count)

    countries_count = winners_sorted(countries_count)
    display_ranking(countries_count)

# most_clubs_with_no_title_countries()

def most_games_for_winless_countries():
    countries = set()
    for values in teams_geo_info.values():
        countries.add(values['country'])
    countries = list(countries)
    countries.remove('tbc')

    for match in data:
        winner = resolve_club_name(match['Winner'])
        if winner == 'Tie':
            continue
        winner_country = teams_geo_info[winner]['country']

        if winner_country in countries:
            countries.remove(winner_country)

    countries_dict = {}
    for match in data:
        home = resolve_club_name(match['Home'])
        away = resolve_club_name(match['Away'])

        home_country = teams_geo_info[home]['country']
        away_country = teams_geo_info[away]['country']

        if home_country == 'Azerbaijan' or away_country == 'Azerbaijan':
            print(home + " - " + away)

        if home_country in countries:
            add_to_counter(home_country, countries_dict)

        if away_country in countries:
            add_to_counter(away_country, countries_dict)

    countries_dict = winners_sorted(countries_dict)
    display_ranking(countries_dict)


most_games_for_winless_countries()