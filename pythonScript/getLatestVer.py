from __future__ import print_function
import pandas as pd
import urllib
import simplejson
import sys

df = pd.read_csv(sys.argv[1])

print('There is a total of %d elements to check' % (len(df)))

# Loop through each row
for x in range(0, len(df)):

    hasVer = False

    # Skip already read elements (in case errno54: Connection reset by peer)
    #if index < 106: continue

    # To keep track the progress
    print('%s %s' % (df.loc[:, 'repo'][x], df.loc[:, 'owner'][x]))

    # Generate API link
    metadataURL = 'https://webcomponents.org/api/meta/%s/%s' % (df.loc[:, 'owner'][x], df.loc[:, 'repo'][x])
    # metadataURL = 'https://webcomponents.org/api/meta/vaadin/vaadin-grid'

    try:
        # Open the URL
        response = urllib.urlopen(metadataURL)

        # Load JSON
        jsonData = simplejson.loads(response.read())
    except simplejson.scanner.JSONDecodeError:
        print('No valid JSON!')
        continue

    if 'version' in jsonData:
        df.loc[:, 'version'][x] = jsonData['version']
        hasVer = True
    else:
        continue

    if hasVer:
        print('Original: %s -> Updated: %s' % (df.loc[:, 'version'][x], jsonData['version']))

df.to_csv('../generated-files/updated.csv', index=False, sep=',')