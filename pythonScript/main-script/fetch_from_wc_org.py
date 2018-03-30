# How to use: Just run the file
# Purpose: This file will get every elements from wc.org to separate JSON file, then merge those JSON files in to a single CSV
# Python 3.6

# Internal library
from commonscript.getjson import get_json_from_url
# External library
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from socket import error as SocketError
import simplejson
import io
import datetime
import os
import errno
import pandas as pd
import glob
import sys

# Define the base URL (wc.org API https://github.com/webcomponents/webcomponents.org/blob/master/API.md)
base = "https://www.webcomponents.org/api/search/kind:element%20kind:element?limit=20&count"
currentURL = base

# Load first JSON to get the total elements number
json_data = get_json_from_url(currentURL)

# Define number of elements per package and get number of total elements
elementCount = json_data["count"]

# Define a counter
counter = 1

# Get value of cursor for the loading of next JSON
nextCursor = json_data["cursor"]

# Getting today date in format (dd-mm-yy)
today = datetime.date.today().strftime('%d-%m-%y')

elementsJSON_path = "/Users/nammeo/Desktop/Vaadin/Projects/web-components-testing/generated-files/elementsJSON/{0}/".format(
    today)

try:
    # If not exist, make the new directory
    os.makedirs(elementsJSON_path)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# while nextCursor is not None:
while counter <= 6:
    #Keep track of progress
    print("{0} {1}\n".format(counter, nextCursor))

    # Get number of elements in results node
    numberOfElements = len(json_data["results"])

    # Name the file with numering start from 01 and following but first
    # element to last element
    JSONFilePath = elementsJSON_path + "%02d_%s->%s.json" % (
        counter, json_data["results"][0]["repo"], json_data["results"][numberOfElements - 1]["repo"])

    # Open it
    with io.open(JSONFilePath, 'w', encoding='utf-8') as f:
        # Remove cursor and count from the JSON
        json_data.pop('cursor', None)
        json_data.pop('count', None)
        # Export to file
        f.write(simplejson.dumps(json_data['results'], ensure_ascii=False))
        f.close()

    # Omit the False: part
    nextCursorValue = nextCursor[6:]
    # Generate the cursor parameter for the URL
    currentURL = "{0}&cursor=False%3A{1}".format(base, nextCursorValue)
    # Read the next JSON
    json_data = get_json_from_url(currentURL)

    # Get value of cursor for the loading of next JSON
    nextCursor = json_data["cursor"]

    # Increase the counter
    counter += 1

# Create a panda frame
frame = pd.DataFrame()

# Load all JSON files in the specific directory
for file in glob.glob(elementsJSON_path + "*.json"):
    pandaObj = pd.read_json(file, encoding='utf-8')
    frame = frame.append(pandaObj, ignore_index=True)

# Name the directory according to the current date
elementsCSV_path = '/Users/nammeo/Desktop/Vaadin/Projects/web-components-testing/generated-files/allElementsCSV'

# Change index=True to get index column at beginning
# A - index;
# F - wc_url (element URL on wc site);
# J - screenshot_url (URL for the screenshot, mostly stored on Vaadin Dropbox);
# K - samplecode_url (URL for the sample code, I was using JSFiddles but later changed to CodePen);
# L - supported_browsers (this needs no explanation);
# M - rating (this too, keep it mind they are really subjective);
# N - (comment, the name explains itself);
# O - external (here lies the links to external document, it could contain multiple links separated by a comma);
# P - polymer (the version of Polymer framework, 0 means no Polymer specified in bower.json or no Polymer use);
# Q - status (I will explain this below);
# R - source (the source of element which I use for importing it online);
# S - bowerjson (the URL to raw bower.json file, have to remove the “.” in the name since it messes with Sami integration code)
frame.to_csv('{0}/allElements_{1}.csv'.format(elementsCSV_path, today), index=False, columns=[
    'repo', 'description', 'owner', 'updated_at', 'version', 'tested_versions', 'wc_url', 'stars', 'forks', 'screenshot_url', 'samplecode_url', 'supported_browsers', 'rating', 'comment', 'external', 'polymer', 'tested', 'included', 'source', 'bowerjson'])
