import os
import numpy as np

from datetime import datetime as dt


def distance(i, j, x, y):
	length = 0
	for k in xrange(i, j - 1):
		a, b = float(x[k + 1]) - float(x[k]), float(y[k + 1]) - float(y[k])
		length += ((a * 96000) ** 2 + (b * 110000) ** 2) ** 0.5
	return length

def period(i, j, timeList):
	time = 0
	for k in range(i, j - 1):
		a, b = dt.strptime(timeList[k], '%H%M%S'), dt.strptime(timeList[k + 1], '%H%M%S')
		time += (b - a).seconds
	return time

def process_raw_data(fname):
	timeList, lonList, latList, occupied = np.loadtxt(fname, delimiter=',', usecols=(1,4,5,9), dtype=str, unpack=True)

	i, n = 0, len(timeList)
	while i < n - 1:
		# trip
		try:
			if occupied[i] == '0' and occupied[i + 1] == '1':
				start, i = i, i + 1
				while i < n and occupied[i] == '1':
					i += 1
				if i == n:
					break

				end = i - 1
				tripLon, tripLat = lonList[start], latList[start]
				tripLength = distance(start, end, lonList, latList)
				tripTime = timeList[start]
				tripPeriod = period(start, end, timeList)

				# cruise 
				if occupied[i - 1] == '1' and occupied[i] == '0':
					start = i - 1
					while i < n and occupied[i] == '0':
						i += 1
					end = i = i - 1
					cruiseLon, cruiseLat = lonList[start], latList[start]
					cruiseLength = distance(start, end, lonList, latList)
					cruiseTime = timeList[start]
					cruisePeriod = period(start, end, timeList)

					fw = open('summary.txt', 'a')
					try:
						tmp = ','.join([fname[4:-4], \
							tripLon[:7], tripLat[:7], tripTime, repr(tripPeriod), repr(tripLength)[:8], \
							cruiseLon[:7], cruiseLat[:7], cruiseTime, repr(cruisePeriod), repr(cruiseLength)[:8]])
					except UnboundLocalError:
						i += 1
						continue
					fw.write(tmp + '\n')
			else:
				i += 1
		except IndexError:
			break

if __name__ == '__main__':
	fList = os.listdir('gps')
	for f in fList:
		process_raw_data('gps/' + f)
		print f[:-4] + ' complete.\n'
