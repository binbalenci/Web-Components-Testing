# How to use: Python 2.7

from __future__ import print_function
import pandas as pd
import urllib
import json

# Read csv
df = pd.read_csv('/Users/nammeo/Desktop/Vaadin/Elements_CSV/unqualified.csv')

# Make a new csv file for storing updated elements
f = open('/Users/nammeo/Desktop/Vaadin/Web-Components Project/autoFetch/updatedElements.csv', 'w')

print('There is a total of %d elements to check' % (len(df)))

# Loop through each row
for index, row in df.iterrows():

	# Define a bool for
	p2 = False 

	# To know the process
	print('%d %s %s' % (index, row['repo'], row['owner']))

	# Generate API link
	metadataURL = 'https://webcomponents.org/api/meta/%s/%s' % (row['owner'], row['repo'])
	#metadataURL = 'https://webcomponents.org/api/meta/vaadin/vaadin-grid'

	# Open the URL
	response = urllib.urlopen(metadataURL)

	# Load JSON
	jsonData = json.loads(response.read())

	if 'bower' in jsonData:
		if 'dependencies' in jsonData['bower']:
				if 'polymer' in jsonData['bower']['dependencies']:
					polymerVer = jsonData['bower']['dependencies']['polymer']
					if "2" in polymerVer:
						f.write('%s,%s,%s,%s\n' % ("", row['repo'],"",row['owner'], jsonData['bower']['version']))
						p2 = True
					else:
						continue
				else:
					continue
		else:
			continue
	else:
		continue

	if p2:
		print('^^^')
	

