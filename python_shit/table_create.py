from datetime import datetime
import json

with open("match_list.json", mode="r", encoding="utf-8") as read_file:
    data = json.load(read_file)

with open("alt_names.json", mode="r", encoding="utf-8") as read_file:
    alt_names = json.load(read_file)

winners_count = {}
leaders_count = {}
most_wins = 0
currentLeader = ""

for match in data:
    if 'Winner' in match and match['Winner'] != 'Tie':
        if match['Winner'] in alt_names:
            name = alt_names[match['Winner']]
        else:
            name = match['Winner']

        if name not in winners_count:
            winners_count[name] = 1
        else:
            winners_count[name] += 1


def winners_sorted(winners_count):
    sorted_list_of_tuples = sorted(
        winners_count.items(),
        key=lambda item: item[1],
        reverse=True
    )

    sorted_winners_count = dict(sorted_list_of_tuples)

    return sorted_winners_count


winners_count = winners_sorted(winners_count)
# print(winners_count)
prev_winner = None
for match in data:
    if match['Winner'] in alt_names:
        winner = alt_names[match['Winner']]
    else:
        winner = match['Winner']

    if winner != 'Tie':
        if prev_winner != winner:
            print(match['Date of match'] + " - " + winner)
        prev_winner = winner

# print(list(winners_count.keys()))

# for team in list(winners_count.keys()):
#     if team in winners_from_website_list:
#         continue
#     print(team)
#
# date_format = '%d/%m/%Y'
# champion_match_count = {}
# champion_time_count = {}
# reign_count = {}
# current_champion = None
# current_starttime = None
# for match in data:
#     if match['Winner'] in alt_names:
#         name = alt_names[match['Winner']]
#     else:
#         name = match['Winner']
#
#
#     if current_champion is None:
#         current_champion = name
#         current_starttime = datetime.strptime(match['Date of match'], date_format)
#         champion_match_count[name] = 0
#         champion_time_count[name] = 0
#         reign_count[name] = 1
#         continue
#
#     if name == 'Tie' or current_champion == name:
#         champion_match_count[current_champion] += 1
#         continue
#
#     if current_champion != name:
#         champion_match_count[current_champion] += 1
#         endtime = datetime.strptime(match['Date of match'], date_format)
#         champion_time_count[current_champion] += (endtime - current_starttime).days
#
#         current_champion = name
#         current_starttime = datetime.strptime(match['Date of match'], date_format)
#         if name not in champion_match_count:
#             champion_match_count[name] = 0
#             champion_time_count[name] = 0
#             reign_count[name] = 1
#         else:
#             reign_count[name] += 1
#
#
# endtime = datetime.now()
# champion_time_count[current_champion] += (endtime - current_starttime).days
#
# champion_match_count = winners_sorted(champion_match_count)
# champion_time_count = winners_sorted(champion_time_count)
# reign_count = winners_sorted(reign_count)

# for team, count in champion_match_count.items():
#     print(team + ": " + str(count))
#
# print("----------------------------------------------")
#
# for team, count in champion_time_count.items():
#     print(team + ": " + str(count))


# for team, count in reign_count.items():
#     print(team + ": " + str(count))

# date_format = '%d/%m/%Y'
# last_date = None
# for match in data:
#     try:
#         datetime.strptime(match['Date of match'], date_format)
#     except ValueError:
#         continue
#
#     if last_date is None:
#         last_date = datetime.strptime(match['Date of match'], date_format)
#         continue
#
#     today = datetime.strptime(match['Date of match'], date_format)
#
#     if (today - last_date).days >= 13:
#         print(last_date.strftime(date_format) + " - " + match['Date of match'] + ": " + str((today - last_date).days))
#     # print((today - last_date).days)
#
#     last_date = today


cities_count = {}
london_count = {}
england = ["London", "Liverpool", "Birmingham", "Sheffield", "Manchester", "Blackburn", "Nottingham", "Burnley",
           "Preston", "Sunderland", "Bolton", "West Bromwich", "Newcastle", "Derby", "Wolverhampton", "Middlesbrough",
           "Huddersfield", "Stoke", "Bury", "Leicester", "Portsmouth", "Bristol", "Bradford", "Leeds", "Blackpool",
           "Oldham", "Luton", "Reading", "Southampton", "Grimsby", "Plymouth", "Hanley"]

barcelona_count = {}

# for match in data:
#     if match['Home'] in alt_names:
#         home = alt_names[match['Home']]
#     else:
#         home = match['Home']
#
#     if match['Away'] in alt_names:
#         away = alt_names[match['Away']]
#     else:
#         away = match['Away']
#
#     city = None
#     if match['Venue'] in ['London', 'Oxford', 'Bingen', 'Homburg']:
#         city = match['Venue']
#
#     if ',' not in match['Venue'] and city is None:
#         if match['Venue'] != 'tbc' and match['Venue'] != 'to be confirmed' and match['Venue'] != "":
#             print(match['Venue'])
#         print(match)
#         continue
#
#     if city is None:
#         city = match['Venue'].split(",")[-1][1:]
#
#     if city == "Beograd":
#         city = "Belgrade"
#     if city in ["Turkey", "Catalonia", "USA", "Saudi Arabia"]:
#         city = match['Venue'].split(",")[1][1:]
#
#     if city in england:
#         continue
#
#     if city not in cities_count:
#         cities_count[city] = 1
#     else:
#         cities_count[city] += 1
#
#     if city == 'London':
#         if match['Venue'] not in london_count:
#             london_count[match['Venue']] = 1
#         else:
#             london_count[match['Venue']] += 1
#
#     # if city == 'Barcelona':
#     #     if match['Venue'] not in barcelona_count:
#     #         barcelona_count[match['Venue']] = 1
#     #     else:
#     #         barcelona_count[match['Venue']] += 1
#
#     if city == 'Madrid':
#         if match['Home'] not in barcelona_count:
#             barcelona_count[match['Home']] = 1
#         else:
#             barcelona_count[match['Home']] += 1
#
# cities_count = winners_sorted(cities_count)
# london_count = winners_sorted(london_count)
# barcelona_count = winners_sorted(barcelona_count)
# # print(cities_count)
#
# i = 1
# for city in cities_count.keys():
#     print(str(i) + ". " + city + " - " + str(cities_count[city]))
#     i += 1
#
# print('--------------------------------')
# # i = 1
# # for london_venue in london_count.keys():
# #     print(str(i) + ". " + london_venue + " - " + str(london_count[london_venue]))
# #     i += 1
#
# i = 1
# for barcelona_venue in barcelona_count.keys():
#     print(str(i) + ". " + barcelona_venue + " - " + str(barcelona_count[barcelona_venue]))
#     i += 1

# games_count_dict = {}
#
# for match in data:
#     if match['Home'] in alt_names:
#         home = alt_names[match['Home']]
#     else:
#         home = match['Home']
#
#     if match['Away'] in alt_names:
#         away = alt_names[match['Away']]
#     else:
#         away = match['Away']
#
#     matchup = " - ".join(sorted([home,away]))
#
#     if matchup in games_count_dict:
#         games_count_dict[matchup] += 1
#     else:
#         games_count_dict[matchup] = 1
#
#
# games_count_dict = winners_sorted(games_count_dict)
# # print(games_count_dict)
#
# place = 1
# last_count = None
# for i, result in enumerate(games_count_dict.items()):
#     if result[1] != last_count:
#         place = i + 1
#         last_count = result[1]
#     print(str(place) + ". " + result[0] + ": " + str(result[1]))

# def addToWinrateDict(club, isWon):
#     if isWon:
#         if club not in winrate_dict:
#             winrate_dict[club] = {'matches': 1, 'wins': 1}
#         else:
#             winrate_dict[club]['matches'] += 1
#             winrate_dict[club]['wins'] += 1
#
#     else:
#         if club not in winrate_dict:
#             winrate_dict[club] = {'matches': 1, 'wins': 0}
#         else:
#             winrate_dict[club]['matches'] += 1
#
#
# winrate_dict = {}
# current_champion = None
#
# for match in data:
#     if match['Home'] in alt_names:
#         home = alt_names[match['Home']]
#     else:
#         home = match['Home']
#
#     if match['Away'] in alt_names:
#         away = alt_names[match['Away']]
#     else:
#         away = match['Away']
#
#     if match['Winner'] in alt_names:
#         winner = alt_names[match['Winner']]
#     else:
#         winner = match['Winner']
#
#     if home != current_champion:
#         challenger = home
#     else:
#         challenger = away
#
#     if challenger == winner:
#         addToWinrateDict(challenger, True)
#     else:
#         addToWinrateDict(challenger, False)
#
#     if current_champion is None or winner != "Tie":
#         current_champion = winner
#
# for club in winrate_dict:
#     winrate_dict[club]['winrate'] = winrate_dict[club]['wins'] / winrate_dict[club]['matches']
#
#
# def winrate_sorted(winrate_dict):
#     sorted_list_of_tuples = sorted(
#         winrate_dict.items(),
#         key=lambda item: (item[1]['winrate'], item[1]['matches']),
#         reverse=True
#     )
#
#     sorted_winrate = dict(sorted_list_of_tuples)
#
#     return sorted_winrate
#
#
# winrate_dict = {k: v for k, v in winrate_dict.items() if v['matches'] >= 10}
# winrate_dict = winrate_sorted(winrate_dict)
#
# place = 1
# last_winrate = None
# last_matches = None
# for i, club in enumerate(winrate_dict):
#     if winrate_dict[club]['winrate'] != last_winrate or winrate_dict[club]['matches'] != last_matches:
#         place = i + 1
#         last_winrate = winrate_dict[club]['winrate']
#         last_matches = winrate_dict[club]['matches']
#     print(str(place) + ". " + club + " (" + str(winrate_dict[club]['wins']) + "/" +
#           str(winrate_dict[club]['matches']) + ")")
