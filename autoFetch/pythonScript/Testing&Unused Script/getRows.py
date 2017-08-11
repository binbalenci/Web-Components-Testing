import sys

first = int(sys.argv[1])
last = int(sys.argv[2])

for x in range(first, last + 1):
	print("%d, " % (x), end='')
