# 29-06-2017 11:35:13 -> 1498736113
# 06-11-2017 11:35:13 -> 1509968113

import random
import time

length = 670
startepoch = 1498736113
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
