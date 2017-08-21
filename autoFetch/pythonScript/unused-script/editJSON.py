import json

JSONpath = "../01.json"
result = []

with open(JSONpath, "rb") as json_data:
	data = json.load(json_data)
	data.pop('cursor', None)
	data.pop('count', None)

with open(JSONpath, 'w') as json_data:
    data = json.dump(data, json_data)