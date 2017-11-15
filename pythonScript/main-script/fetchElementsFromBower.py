# Python 2.7
import urllib
import simplejson
import re
import sys
import time
import multiprocessing

# Create a pool with n processors
pool = multiprocessing.Pool(processes=2)

# Get the start time
starttime = time.time()
lasttime = 0
elapsedtime = 0
registrytime = 0

# Define an index for keeping track
index = 0

# Define a counter to count how many web-components the regex is detecting
wccount = 0

# Make a new text file to record all the web-components
f = open("/Users/nammeo/Desktop/Vaadin/Projects/web-components-testing/generated-files/bower-web-components.txt", "w")

# Define a boolean to check dependencies after checking keywords
checkDependencies = True

# Define a list of keywords to check
wckeywords = ["web-components", "web-component", "custom-element", "custom-elements", "polymer"]

# Read full bower package json
bowerregistry = "https://registry.bower.io/packages"

try:
    response = urllib.urlopen(bowerregistry)
    # Load it into json
    packagesjson = simplejson.loads(response.read()) # Now the whole bower registry json is stored in packagejson

    registrytime = time.time() - starttime
    lasttime += registrytime
    print("Time taken for storing bower packages json: {0} second(s)".format(registrytime))
except simplejson.scanner.JSONDecodeError:
    print('No valid JSON in Bower registry. Quitting!')
    sys.exit(0)

# Define a regex for the repo URL
repoRegex = r"(https:\/\/github.com)(\/)([^:\/\s]+)(\/)([^:\/\s]+)(.git)"

p = re.compile(repoRegex, re.IGNORECASE)

print('There is a total of {0} repos to check'.format(len(packagesjson)))

for i in range(len(packagesjson)):
    currentRepo = packagesjson[i]['url']

    # To keep track the progress
    print('{0} {1}'.format(index, currentRepo))
    index += 1

    if index % 10 == 0:
        elapsedtime = time.time() - lasttime
        lasttime += elapsedtime
        print("Time taken for batch of 10: {0} second(s)".format(elapsedtime))

    # Check if the repository is from github
    matchedString = p.match(packagesjson[i]['url'])

    # Matched String is splitted into several RegExp groups
    # 0: whole matchedString
    # 3: owner
    # 5: repo

    if matchedString:
        bowerjsonrawlink = "https://rawgit.com/{0}/{1}/master/bower.json".format(matchedString.group(3), matchedString.group(5))
    else:
        print("Not Github repo!")
        continue

    try:
        # Open the URL
        response = urllib.urlopen(bowerjsonrawlink)

        # Load JSON
        packagejson = simplejson.loads(response.read())
    except simplejson.scanner.JSONDecodeError:
        print('No bower.json!')
        continue

    # Checking JSON children if there are version of polymer available in JSON data
    # Also get the version from JSON to guarantee it's the latest version
    if 'keywords' in packagejson:
        checkDependencies = True
        # Converting things to lowercase for the sake of using `in`
        keywords = [x.lower() for x in packagejson['keywords']]
        # Define a variable for checking if the keywords section contains any keywords related to web-compoents
        hasKeyword = any(x in wckeywords for x in keywords)
        if hasKeyword:
            print("Qualified")
            wccount += 1
            checkDependencies = False
            f.write("{0}\n".format(currentRepo))
    else:
        print("No keywords found!")

    if 'dependencies' in packagejson and checkDependencies:
        # Converting things to lowercase for the sake of using `in`
        dependencies = [x.lower() for x in packagejson['dependencies']]
        if 'polymer' in dependencies: # Converting everything to lowercase
            print("Qualified")
            wccount += 1
            f.write("{0}\n".format(currentRepo))
    else:
        continue

f.close()
print("Time taken: {0} seconds".format(lasttime))
print("Number of elements found: {0}".format(wccount))
