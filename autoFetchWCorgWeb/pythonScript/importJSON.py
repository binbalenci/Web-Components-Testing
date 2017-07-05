#python2
import urllib, json, io
# Define the base URL
base = "https://www.webcomponents.org/api/search/kind:element%20kind:element?limit=20&count"
currentURL = base

# Load first JSON
response = urllib.urlopen(currentURL)
data = json.loads(response.read())

# Define number of elements per package and get number of total elements
packageCount = 20
elementCount = data["count"]
timeOfLoop = elementCount/packageCount + 1

print len(data["results"])
# print data["results"][18]["repo"]

# Get cursor value and get the next JSON
for x in range(1, timeOfLoop + 1):
	numberOfElements = len(data["results"])
	with io.open('elementsJSONs/%02d_%s->%s.json' % (x, data["results"][0]["repo"], data["results"][numberOfElements - 1]["repo"]), 'w', encoding='utf-8') as f:
  		f.write(json.dumps(data, ensure_ascii=False))

	nextCursor = data["cursor"]

	if nextCursor is not None:
		print `x` + " " + nextCursor + "\n"
		nextCursorValue = data["cursor"][6:]
		currentURL = base + "&cursor=False%3A" + nextCursorValue
		response = urllib.urlopen(currentURL)
		data = json.loads(response.read())
		# print len(data["results"])
		x += 1
	else:
		break
