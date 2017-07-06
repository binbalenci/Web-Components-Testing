#python2
import urllib, json, io

# Define the base URL
URLs = ["https://raw.githubusercontent.com/a1626/image-carousel/master/bower.json","https://raw.githubusercontent.com/PolymerEl/firebase-nest/master/bower.json"]
result = []

# Loop to load JSON
for x in range(0, len(URLs)):
	response = urllib.urlopen(URLs[x])
	data = json.loads(response.read())
	result.append(data["name"])

with open("../allTags.json", "wb") as outfile:
     json.dump(result, outfile)

#print data["keywords"]