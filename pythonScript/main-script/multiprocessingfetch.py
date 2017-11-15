# Python 2.7
from __future__ import print_function
import urllib
import simplejson
import re
import sys
import time
import multiprocessing as mp
import time
from socket import error as SocketError
import errno

# Define a list of keywords to check
wckeywords = ["web-components", "web-component", "custom-element", "custom-elements", "polymer"]

# Define a boolean to check dependencies after checking keywords
checkDependencies = True

# Define a regex for the repo URL
repoRegex = r"(https:\/\/github.com)(\/)([^:\/\s]+)(\/)([^:\/\s]+)(.git)"

p = re.compile(repoRegex, re.IGNORECASE)

def checkElement(url):
    global checkDependencies

    print("{0}".format(url))

    # Make a new text file to record all the web-components
    f = open("/Users/nammeo/Desktop/Vaadin/Projects/web-components-testing/generated-files/bower-web-components.txt", "a")

    # Check if the repository is from github
    matchedString = p.match(url)

    # Matched String is splitted into several RegExp groups
    # 0: whole matchedString
    # 4: owner
    # 6: repo
    # for i in range(0,7):
    #     print(str(i) + " " + matchedString.group(i))

    if matchedString:
        bowerjsonrawlink = "https://rawgit.com/{0}/{1}/master/bower.json".format(matchedString.group(3), matchedString.group(5))
    else:
        # print("Not Github repo! ", end="")
        return False

    try:
        # Open the URL
        response = urllib.urlopen(bowerjsonrawlink)
        # Load JSON
        packagejson = simplejson.loads(response.read())
    except simplejson.scanner.JSONDecodeError:
        # print('No bower.json! ', end="")
        return False
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise # Not error we are looking for
        # Handle error here.
        checkElement(url)

    # Checking JSON children if there are version of polymer available in JSON data
    # Also get the version from JSON to guarantee it's the latest version
    if 'keywords' in packagejson:
        checkDependencies = True
        # Check if keywords is empty
        if packagejson['keywords']:
            # Converting things to lowercase for the sake of using `in`
            keywords = [x.lower() for x in packagejson['keywords']]
            # Define a variable for checking if the keywords section contains any keywords related to web-compoents
            hasKeyword = any(x in wckeywords for x in keywords)
            if hasKeyword:
                # print("Qualified! ", end="")
                checkDependencies = False
                f.write("{0}\n".format(url))
                return True
        # else:
            # print("No keywords found! ", end="")

    if 'dependencies' in packagejson and checkDependencies:
        # Check if dependencies is empty
        if packagejson['dependencies']:
            # Converting things to lowercase for the sake of using `in`
            dependencies = [x.lower() for x in packagejson['dependencies']]
            if 'polymer' in dependencies: # Converting everything to lowercase
                # print("Qualified")
                # wccount += 1
                f.write("{0}\n".format(url))
                return True
    else:
        # print("No dependencies found! ", end="")
        return False

    f.close()

# Read full bower package json
bowerregistry = "https://registry.bower.io/packages"

try:
    response = urllib.urlopen(bowerregistry)
    # Load it into json
    packages = simplejson.loads(response.read()) # Now the whole bower registry json is stored in packagejson
except simplejson.scanner.JSONDecodeError:
    print('No valid JSON in Bower registry. Quitting!')
    sys.exit(0)

# Get the repos URL
urls = [packages[i]['url'] for i in range(len(packages))]


if __name__ == "__main__":
    print("There are a total of {0} repos to check.".format(len(urls)))

    # Create a pool with n processors
    pool = mp.Pool(processes=8)

    # Get the start time
    starttime = time.time()

    r = pool.map(checkElement, urls)
    # for i in range(len(urls)):
    #     print(i, end=" ")
    #     pool.apply_async(checkElement, args = (urls[i], ))
    pool.close()
    pool.join()

    elapsedtime = time.time() - starttime

    print("Times taken: {0}".format(elapsedtime))
