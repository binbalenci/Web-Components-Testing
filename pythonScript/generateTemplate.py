# Python 2.7
# Purpose: this file is to generate the import for codepen/jsfiddle/jsbin temaplate (the template includes <base> tag, html import, polyfill import)

from __future__ import print_function
import pandas as pd
import sys

df = pd.read_csv(sys.argv[1])

f = open('/Users/nammeo/Desktop/Vaadin/Projects/web-components-testing/generated-files/template.csv', 'w+')

# Loop through each row
for x in range(0, len(df)):

    # To keep track the progress
    print('%s %s' % (df.loc[:, 'repo'][x], df.loc[:, 'owner'][x]))

    f.write('<base href="https://polygit.org/{0}+{1}+{2}/components/"><script src="webcomponentsjs/webcomponents-lite.js"></script><link rel="import" href="{0}/{0}.html">\n'.format(df.loc[:, 'repo'][x], df.loc[:, 'owner'][x], df.loc[:, 'version'][x]))
