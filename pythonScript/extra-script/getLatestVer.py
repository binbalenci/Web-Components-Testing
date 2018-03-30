# Python 2.7
# Purpose: to get the latest version of the component imported for correct links to bowerjson and demo file
# this piece of code is only to update the already-imported version. For future integration, things should be done in JSONtoCSV.py

import pandas as pd
from urllib.request import urlopen
import simplejson
import sys

df = pd.read_csv(sys.argv[1], converters={'index': str, 'stars': str, 'forks': str, 'polymer' : str})

print('There is a total of %d elements to check' % (len(df)))

# Loop through each row
for x in range(0, len(df)):

    hasVer = False
    sameVer = True
    startmessage = ''
    endmessage = ''
    currentVer = df.loc[:, 'version'][x]

    # Skip already read elements (in case errno54: Connection reset by peer)
    # if x < 170: continue

    # To keep track the progress
    startmessage = '{2} {0} {1}'.format(df.loc[:, 'repo'][x], df.loc[:, 'owner'][x], x)
    print(startmessage, end='')

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

    if 'version' in jsonData:
        hasVer = True
        if df.loc[:, 'version'][x] != jsonData['version']:
            df.loc[:, 'version'][x] = jsonData['version']
            sameVer = False
    else:
        continue

    # Add version number to beginning of comment
    commentisnan = pd.isnull(df.loc[:, 'comment'][x])
    df.loc[:, 'comment'][x] = '{0}: {1}'.format(df.loc[:, 'version'][x], '' if commentisnan else df.loc[:, 'comment'][x])

    if hasVer == True and sameVer == False:
        endmessage = 'Original: {0} -> Updated: {1}'.format(currentVer, jsonData['version'])
        print(endmessage.rjust(50, '-'))
    elif hasVer == True and sameVer == True:
        endmessage = 'No new version!'
        print(endmessage.rjust(50, '-'))
    elif hasVer == False:
        endmessage = 'No version detected!'
        print(endmessage.rjust(50, '-'))

    df.to_csv('/Users/nammeo/Desktop/Vaadin/Projects/web-components-testing/generated-files/updated.csv', index=False, sep=',')
