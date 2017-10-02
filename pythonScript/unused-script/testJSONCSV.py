import json
import csv
import sys
import glob
import os.path
import datetime
import errno
import io

# Getting today date in format (dd-mm-yy)
today = datetime.date.today().strftime('%d-%m-%y')

try:
    # Name the directory according to the current date
    directoryPath = "/Users/nammeo/Desktop/Vaadin/Web-Components Project/autoFetch/elementsCSV_%s/" % (
        today)
    # If not exist, make the new directory
    os.makedirs(directoryPath)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# Load all JSON files in the specific directory
for file in glob.glob(sys.argv[1] + "*.json"):
    with io.open(file, 'r') as infile:
        elements_JSON = json.load(infile)["results"]
        # print elements_JSON

    # Get filename without extension
    fileName = os.path.splitext(os.path.basename(file))[0]

    with open('%s%s.csv' % (directoryPath, fileName), 'w+') as outfile:
    	csv_writer = csv.writer(outfile)
    	isHeader = True

    	for element in elements_JSON:
    		print element
    		if isHeader == True:
    			header = element.keys()
    			csv_writer.writerow(header)
    			isHeader = False
			csv_writer.writerow(element.values())
		outfile.close()



# element_parsed = json.loads(element_JSON)
# element_data = element_parsed["results"]
# # print json_parsed['email']

# with open('parsedJSON.csv', 'w+') as employ_data:
#     csv_writer = csv.writer(employ_data)
#     count = 0

#     for emp in element_data:
# 		if count == 0:
# 			header = emp.keys()
# 	        csv_writer.writerow(header)
# 	        count += 1
# 		csv_writer.writerow(emp.values())
#     employ_data.close()
