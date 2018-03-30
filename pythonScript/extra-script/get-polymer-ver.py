# Python 3.6
# Purpose: to get the latest version of the component imported for correct links to bowerjson and demo file
# this piece of code is only to update the already-imported version. For future integration, things should be done in JSONtoCSV.py

import pandas as pd
from urllib.request import urlopen
import simplejson
import sys
import re

# Define a regex for Polymer 2 version which will match these (>=2.0.0-rc.2 <3.0; ^2.0.0; 1.9 - 2; ^1.0.0 || ^2.0.0; 2.0.0; ^2; ^2.0.2; 2.0.0-rc.3; 1 - 2, 2.1.0)
polymer2Regex = r"(\^2)|(\-\s*2)|([^.]2\.)|(^2.)"

df = pd.read_csv(sys.argv[1], converters={'index': str, 'stars': str, 'forks': str, 'polymer' : str})

print('There is a total of %d elements to check' % (len(df)))

# Loop through each row
for x in range(0, len(df)):
    # Skip already read elements (in case errno54: Connection reset by peer)
    # if x < 170: continue

    # To keep track the progress
    print('{0} {1} {2}'.format(x, df.loc[:, 'repo'][x], df.loc[:, 'owner'][x]))

    # Generate API link
    metadataURL = 'https://webcomponents.org/api/meta/%s/%s' % (df.loc[:, 'owner'][x], df.loc[:, 'repo'][x])
    # metadataURL = 'https://webcomponents.org/api/meta/vaadin/vaadin-grid'

    try:
        # Open the URL
        response = urlopen(metadataURL)

        # Load JSON
        jsonData = simplejson.loads(response.read())
    except simplejson.scanner.JSONDecodeError:
        print('No valid JSON!')
        continue

    try:
        if 'polymer' in jsonData['bower']['dependencies']:
            polymerVer = jsonData['bower']['dependencies']['polymer']
            if re.search(polymer2Regex, polymerVer):
                df.loc[:, 'polymer'][x] = "2"
                print("2")
            else:
                df.loc[:, 'polymer'][x] = "1"
                print("1")
        else:
            df.loc[:, 'polymer'][x] = "0"
            print("0")
    except Exception as e:
        # print(e.code)
        # print(e.read)
        continue

    df.to_csv('/Users/nammeo/Desktop/Vaadin/Projects/web-components-testing/generated-files/updated.csv', index=False, sep=',')
