import json

with open("teams_geo_info.json", mode="r", encoding="utf-8") as read_file:
    data = json.load(read_file)


print(len(data))