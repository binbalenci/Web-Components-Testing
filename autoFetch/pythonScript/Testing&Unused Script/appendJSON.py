import json
import glob
import sys
import datetime

result = []

for file in glob.glob(sys.argv[1] + "*.json"):
    with open(file, "rb") as infile:
        result.append(json.load(infile))

# Getting today date in format (dd-mm-yy)
today = datetime.date.today().strftime('%d-%m-%y')

with open("../allElementsJSON/allElements_%s.json" % (today), "wb") as outfile:
     json.dump(result, outfile)
