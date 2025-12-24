import json

with open("match_list.json", mode="r", encoding="utf-8") as read_file:
    data = json.load(read_file)

with open("alt_names.json", mode="r", encoding="utf-8") as read_file:
    alt_names = json.load(read_file)


teams_geo_info = {}

for match in data:
    home = match['Home']
    away = match['Away']

    if home in alt_names:
        home = alt_names[home]

    if away in alt_names:
        away = alt_names[away]

    if home not in teams_geo_info:
        teams_geo_info[home] = {'country': '', 'city': ''}

    if away not in teams_geo_info:
        teams_geo_info[away] = {'country': '', 'city': ''}

with open('teams_geo_info.json', 'w', encoding='utf-8') as f:
    json.dump(teams_geo_info, f, ensure_ascii=False, indent=4)

