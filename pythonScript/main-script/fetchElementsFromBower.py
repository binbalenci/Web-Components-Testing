# Python 2.7
import urllib
import simplejson
import re
import sys

# Define an index for keeping track
index = 0

# Define a counter to count how many web-components the regex is detecting
wccount = 0

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
except simplejson.scanner.JSONDecodeError:
    print('No valid JSON in Bower registry. Quitting!')
    sys.exit(0)

# Define a regex for the repo URL
repoRegex = r"(https:\/\/github.com)(\/)([^:\/\s]+)(\/)([^:\/\s.]+)(.git)"

p = re.compile(repoRegex, re.IGNORECASE)

print('There is a total of {0} repos to check'.format(len(packagesjson)))

for i in range(0, len(packagesjson)):
    # To keep track the progress
    print('{0} {1}'.format(index, packagesjson[i]['url']))
    index += 1

    # Check if the repository is from github
    matchedString = p.match(packagesjson[i]['url'])

    # Matched String is splitted into several RegExp groups
    # 0: whole matchedString
    # 3: owner
    # 5: repo

    if matchedString:
        bowerjsonrawlink = "https://rawgit.com/{0}/{1}/master/bower.json".format(matchedString.group(3), matchedString.group(5))
    else:
        print("Not Github!")
        continue

    try:
        # Open the URL
        response = urllib.urlopen(bowerjsonrawlink)

        # Load JSON
        packagejson = simplejson.loads(response.read())
    except simplejson.scanner.JSONDecodeError:
        print('No valid JSON!')
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
    else:
        pass

    if 'dependencies' in packagejson and checkDependencies:
        # Converting things to lowercase for the sake of using `in`
        dependencies = [x.lower() for x in packagejson['dependencies']]
        if 'polymer' in dependencies: # Converting everything to lowercase
            print("Qualified")
            wccount += 1
    else:
        continue

print("Number of elements found: {0}".format(wccount))
