import json
import glob

result = []
for f in glob.glob("../elementsJSONs/*.json"):
    with open(f, "rb") as infile:
        result.append(json.load(infile))

with open("allElements.json", "wb") as outfile:
     json.dump(result, outfile)