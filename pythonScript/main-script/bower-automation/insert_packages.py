import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import sys
import simplejson
import re
from urllib.request import urlopen

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

# Make a connection to database
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

data = '[{"name":"0x100-angular-steps","url":"https://github.com/0x100/angular-steps.git"},{"name":"10digit-geo","url":"https://github.com/10digit/geo.git"},{"name":"10digit-invoices","url":"https://github.com/10digit/invoicesV"},{"name":"2klic_graphics_icons","url":"https://jolava@bitbucket.org/2klicdev/graphics_icons.git"},{"name":"vaadin-button","url":"https://github.com/vaadin/vaadin-button.git"}]'
packages = simplejson.loads(data)

# # Read full bower package json
# bowerregistry = "https://registry.bower.io/packages"
#
# try:
#     # Retrieve the whole content from bower registry
#     data = urlopen(bowerregistry).read()
#     # Load it into json
#     packages = simplejson.loads(data) # Now the whole bower registry json is stored in packages
# except simplejson.scanner.JSONDecodeError:
#     print('No valid JSON in Bower registry. Quitting!')
#     sys.exit(0)


# checked_time = datetime.now()
# Define a regex for the repo URL
repoRegex = r"^(https:\/\/github\.com)(\/)([^:\/\s]+)(\/)([^:\/\s]+?)(\.git)?$"

p = re.compile(repoRegex, re.IGNORECASE)

for package in packages:
    url = package['url']

    matchedString = p.match(url)

    if matchedString:
        repo = matchedString.group(5)
        owner = matchedString.group(3)
        package_id = "{0}_{1}".format(owner, repo)
        is_github = 1
    else:
        repo = ""
        owner = ""
        package_id = ""
        is_github = 0

    add_package = (
        "INSERT INTO registry "
        "(repo, owner, url, is_github, package_id) "
        "VALUES (%(repo)s, %(owner)s, %(url)s, %(is_github)s, %(package_id)s)"
    )

    data_package = {
        'repo': repo,
        'owner': owner,
        'url': url,
        'is_github': is_github,
        'package_id': package_id
    }

    cursor.execute(add_package, data_package)

    cnx.commit()

cursor.close()
cnx.close()
