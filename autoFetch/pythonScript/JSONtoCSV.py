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
    directoryPath = '/Users/nammeo/Desktop/Vaadin/Web-Components Project/autoFetch/allElementsCSV/'
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
    # Get filename without extension
    # fileName = os.path.splitext(os.path.basename(file))[0]

frame.to_csv('%sallElements_%s.csv' % (directoryPath, today), index=False, columns=[
    'repo', 'description', 'owner', 'version', 'wc_url', 'updated_at', 'stars', 'forks', 'screenshot_url', 'samplecode_url', 'supported_browsers', 'rating', 'comment', 'external', 'status'])
