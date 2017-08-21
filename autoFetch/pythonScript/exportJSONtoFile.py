# How to use: Just run the file
# Python 2.7

import urllib
import json
import io
import datetime
import os
import errno

# Define the base URL
base = "https://www.webcomponents.org/api/search/kind:element%20kind:element?limit=20&count"
currentURL = base

# Get the current working directory
# cwd = os.getcwd()
# path = os.path.abspath(os.chdir(".."))
# print path

# Load first JSON to get the total elements number
response = urllib.urlopen(currentURL)
data = json.loads(response.read())

# Define number of elements per package and get number of total elements
packageCount = 20
elementCount = data["count"]

# Define time of looping
timeOfLoop = elementCount / packageCount + 1

# Getting today date in format (dd-mm-yy)
today = datetime.date.today().strftime('%d-%m-%y')

# print len(data["results"])
# print data["results"][18]["repo"]

try:
    # Name the directory according to the current date
    directoryPath = "/Users/nammeo/Desktop/Vaadin/Web-Components Project/autoFetch/elementsJSON_%s/" % (
        today)
    # If not exist, make the new directory
    os.makedirs(directoryPath)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

for counter in range(1, timeOfLoop + 1):
    # Get number of elements in results node
    numberOfElements = len(data["results"])

    # Get value of cursor for the loading of next JSON
    nextCursor = data["cursor"]

    # Name the file with numering start from 01 and following but first
    # element to last element
    JSONFilePath = directoryPath + "%02d_%s->%s.json" % (
        counter, data["results"][0]["repo"], data["results"][numberOfElements - 1]["repo"])

    # Open it
    with io.open(JSONFilePath, 'w', encoding='utf-8') as f:
        # Remove cursor and count from the JSON
        data.pop('cursor', None)
        data.pop('count', None)
        # Export to file
        f.write(json.dumps(data['results'], ensure_ascii=False))

        # Check if there is a next cursor value
    if nextCursor is not None:
        print `counter` + " " + nextCursor + "\n"
        # Omit the False: part
        nextCursorValue = nextCursor[6:]
        # Generate the cursor parameter for the URL
        currentURL = base + "&cursor=False%3A" + nextCursorValue
        # Read the next JSON
        response = urllib.urlopen(currentURL)
        data = json.loads(response.read())
        # print len(data["results"])
        counter += 1
    else:
        break
