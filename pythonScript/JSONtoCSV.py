#How to use: Run with python3, input the JSON folder into the 2nd argument

import pandas as pd
import os
import errno
import datetime
import glob
import sys

# Getting today date in format (dd-mm-yy)
today = datetime.date.today().strftime('%d-%m-%y')

try:
    # Name the directory according to the current date
    directoryPath = '/Users/nammeo/Desktop/Vaadin/Projects/web-components-testing/generated-files/allElementsCSV/'
    # If not exist, make the new directory
    os.makedirs(directoryPath)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

frame = pd.DataFrame()
# Load all JSON files in the specific directory
for file in glob.glob(sys.argv[1] + "*.json"):
    pandaObj = pd.read_json(file, encoding='utf-8')
    frame = frame.append(pandaObj, ignore_index=True)

    #EXPERIMENT: Encode emoji to unicode
    frame['description'] = frame['description'].map(lambda x: x.encode('utf-8'))

    # Get filename without extension
    # fileName = os.path.splitext(os.path.basename(file))[0]

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

frame.to_csv('%sallElements_%s.csv' % (directoryPath, today), index=True, columns=[
    'repo', 'description', 'owner', 'version', 'wc_url', 'updated_at', 'stars', 'forks', 'screenshot_url', 'samplecode_url', 'supported_browsers', 'rating', 'comment', 'external', 'polymer', 'status', 'source', 'bowerjson'])
