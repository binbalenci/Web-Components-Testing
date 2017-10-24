# Python 2.7
# Purpose: this file is to convert description text to raw value utf-8 since it contains emojis and our DB does not support 4-byte UTf-8 (Only 3-byte UTF-8)
# this piece of code is only to convert the already-imported description to raw value. For future integration, things should be done in JSONtoCSV.py

from __future__ import print_function
import pandas as pd
import sys

df = pd.read_csv(sys.argv[1])

print('There is a total of %d elements to convert' % (len(df)))

# Loop through each row
for x in range(0, len(df)):

    # hasVer = False

    # Skip already read elements (in case errno54: Connection reset by peer)
    # if index < 106: continue

    # To keep track the progress
    print('%s %s' % (df.loc[:, 'repo'][x], df.loc[:, 'owner'][x]))

    # Convert description to raw utf-8 value
    df['description'] = df['description'].map(lambda x: x.encode('utf-8'))

	# Add version number to beginning of comment
    #df.loc[:, 'comment'][x] = '{0}: {1}'.format(df.loc[:, 'version'][x], df.loc[:, 'comment'][x])

df.to_csv('../generated-files/updated.csv', index=False, sep=',')
