from datetime import datetime
import json

with open("match_list.json", mode="r", encoding="utf-8") as read_file:
    data = json.load(read_file)


with open("alt_names.json", mode="r", encoding="utf-8") as read_file:
    alt_names = json.load(read_file)

date_format = '%d/%m/%Y'
print(len(data))
