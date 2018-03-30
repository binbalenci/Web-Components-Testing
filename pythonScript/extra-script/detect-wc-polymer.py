# Python 3.6
# Purpose: this file will get all the wc from db through query, then detect which Polymer the webcomponent is using.

from socket import error as SocketError
import mysql.connector
import sys
import re
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from simplejson.scanner import JSONDecodeError
import simplejson
import errno
import time
import multiprocessing as mp

# Define a regex for Polymer 2 version which will match these (>=2.0.0-rc.2 <3.0; ^2.0.0; 1.9 - 2; ^1.0.0 || ^2.0.0; 2.0.0; ^2; ^2.0.2; 2.0.0-rc.3; 1 - 2, 2.1.0)
polymer2_regex = r"(\^2)|(\-\s*2)|([^.]2\.)|(^2.)"
polymer1_regex = r"(\^1)|(\-\s*1)|([^.]1\.)|(^1.)"
polymer0_regex = r"(\^0)|(\-\s*0)|([^.]0\.)|(^0.)"

### GLOBAL section
# Define the database name
DB_NAME = 'bower_packages'

# Define the config for database connection
config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': DB_NAME,
    'raise_on_warnings': True
}

### Define a list of keywords for separte framework

# Polymer
polymer_keywords = ["polymer"]

### List ENDS

# Define a boolean to check keywords after checking dependencies
check_keywords = True

# Query for adding checked time
add_library = (
    "UPDATE registry "
    "SET library = %s "
    "WHERE url = %s"
)

# Should be fairly straightforward, just check an element bower.json. The parameter `package` is json
def check_library(package):
    # Store the values to simpler name for easy future use (except id because that's Python reserved name)
    repo = package['repo']
    owner = package['owner']
    url = package['url']

    # Define cursor for executing query
    curB = cnx.cursor(buffered=True, dictionary=True)

    # Keep track of the progress
    print("{0} {1}".format(package['id'], url))

    # Generate the raw bower.json link using rawgit.com. Is it reliable enough?
    bower_json_link = "https://rawgit.com/{0}/{1}/master/bower.json".format(owner, repo)

    try:
        # Retrieve the content read from bower.json
        data = urlopen(bower_json_link).read()
        # Loads it into a JSON
        package_json = simplejson.loads(data, encoding='latin-1')
    # Check if there is a file named bower.json or the file is readable
    except JSONDecodeError:
        curB.execute(add_library, ("No bower.json", url))
        cnx.commit()
        return
    # Check if the link is reachable
    except HTTPError as e:
        print(e.code)
        curB.execute(add_library, ("Can not reach bower.json", url))
        cnx.commit()
        return
    except SocketError as e:
        print("Socket Error")
        print(e)

    check_keywords = True

    ### FIRST CONDITION STARTS: Check if there is polymer in dependencies. If there is, add checked and is_wc. If not, add is_wc and checked.
    if 'dependencies' in package_json:
        dependencies = package_json['dependencies']
        if dependencies:
            # Converting things to lowercase for the sake of using `in`
            dependencies = [x.lower() for x in package_json['dependencies']]
            if 'polymer' in dependencies:
                polymer_ver = package_json['dependencies']['polymer']
                if re.search(polymer2_regex, polymer_ver):
                    print("Polymer 2!")
                    curB.execute(add_library, ("polymer 2", url))
                    cnx.commit()
                elif re.search(polymer1_regex, polymer_ver):
                    print("Polymer 1!")
                    curB.execute(add_library, ("polymer 1", url))
                    cnx.commit()
                elif re.search(polymer0_regex, polymer_ver):
                    print("Polymer 0!")
                    curB.execute(add_library, ("polymer 0", url))
                    cnx.commit()
                else:
                    print("Polymer Unknown!")
                    curB.execute(add_library, ("polymer", url))
                    cnx.commit()
                return
            else:
                print("No matched dependencies!")
        else:
            print("Empty dependencies!")
    ### FIRST CONDITION ENDS
    else:
        print("No dependencies available!")

    ### SECOND CONDITION STARTS: Check if there is keywords in bower.json. If there is, check if any of the legit keywords appearing there
    if 'keywords' in package_json and check_keywords:
        keywords = package_json['keywords']
        if keywords:
            # Converting things to lowercase for the sake of using `in`
            # Double check if x is null or x is not string
            keywords = [x.lower() for x in keywords if x is not None and isinstance(x, str)]
            # Define a variable for checking if the keywords section contains any keywords related to web-compoents
            hasKeyword = any(x in polymer_keywords for x in keywords)
            if hasKeyword:
                print("Polymer unknown!")
                checkDependencies = False
                curB.execute(add_library, ("polymer", url))
                cnx.commit()
                return
            else:
                print("No matched keywords!")
        ### SECOND CONDITION ENDS: Do nothing, program will move on fourth condition
        else:
            print("Empty keywords!")
    else:
        print("No keywords available!")

    curB.close()

# Running the main function here
if __name__ == "__main__":
    # Get the start time
    starttime = time.time()

    # Make a connection to database
    cnx = mysql.connector.connect(**config)

    # Define cursor for executing query
    curA = cnx.cursor(buffered=True, dictionary=True)

    # Get the begin and end id from Arguments
    # Make a if else condition for end_id so that if user only enters one number, it checks only that id
    begin_id = sys.argv[1]
    end_id = sys.argv[2]

    # query = ("SELECT * FROM registry WHERE is_wc = 1 AND library IS NULL LIMIT {0},{1}".format(begin_id, end_id))
    query = ("SELECT * FROM registry WHERE is_wc = 1 AND library IS NULL LIMIT {0},{1}".format(begin_id, end_id))

    curA.execute(query)

    # Get number of rows from SELECT
    num_rows = curA.rowcount

    # Print the number of rows to check
    print("There are a total of {0} urls to check.".format(num_rows))

    # Create a pool with 8 processors
    pool = mp.Pool(processes=8)

    for package in curA:
        # check_element(package)
        pool.apply(check_library, args = (package, ))

    # Get the running time of the function
    elapsedtime = time.time() - starttime

    print("Times taken: {0} seconds for {1} urls".format(elapsedtime, num_rows))

    # Closing the cursor
    curA.close()
    # Closing DB connection
    cnx.close()
    # Closing the pool
    pool.close()
    pool.join()
