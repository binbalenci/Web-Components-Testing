# Python 2.7 or 3 (whatever, I have not tested with 3 yet)
# Purpose: this script is to generate random unique epoch date for the spreadsheet
import random
import time

length = 670
# 29-06-2017 11:35:13 -> 1498736113
startepoch = 1498736113
# 06-11-2017 11:35:13 -> 1509968113
endepoch = 1509968113

randomEpochDates = random.sample(range(startepoch, endepoch), length)

try:
    f = open('/Users/nammeo/Desktop/Vaadin/Projects/web-components-testing/generated-files/randomDate.csv', 'w+')

    for i in range(len(randomEpochDates)):
        # randomDate = randint(startepoch, endepoch)
        currentEpochDate = randomEpochDates[i]
        converted = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(currentEpochDate))
        f.write('{0},\n'.format(converted))

except OSError as e:
    if e.errno != errno.EEXIST:
        raise

f.close()
