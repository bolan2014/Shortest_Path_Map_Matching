import os

from math import radians, cos, sin, asin, sqrt
from datetime import datetime


def read_road_info(fname, roadNet):
	fr = open(fname, 'r')

	for line in fr:
		road = line.split(',')
		id = road[0]
		length = road[2]
		roadNet[id] = length

def read_track_info(fname, timeList):
	fr = open(fname, 'r')

	for line in fr:
		track = line.split(',')
		#lon = float(track[1])
		#lat = float(track[2])
		#id = int(track[3])
		time = track[4][-7:-1]
		timeList.append(time)

def read_path_info(fname, pathList):
	fr = open(fname, 'r')	

	for line in fr:
		path = line.split(',')
		pathList.append(path[1][:-1])

def trip_time_seconds(timeList):
	start = datetime.strptime(timeList[0], '%H%M%S')
	end = datetime.strptime(timeList[len(timeList)-1], '%H%M%S')

	return (end - start).seconds
	

def time_zones(time):
	if 0 <= time and time < 10000:
		return 0
	elif 10000 <= time and time < 20000:
		return 1
	elif 20000 <= time and time < 30000:
		return 2
	elif 30000 <= time and time < 40000:
		return 3
	elif 40000 <= time and time < 50000:
		return 4
	elif 50000 <= time and time < 60000:
		return 5
	elif 60000 <= time and time < 70000:
		return 6
	elif 70000 <= time and time < 80000:
		return 7
	elif 80000 <= time and time < 90000:
		return 8
	elif 90000 <= time and time < 100000:
		return 9
	elif 100000 <= time and time < 110000:
		return 10
	elif 110000 <= time and time < 120000:
		return 11
	elif 120000 <= time and time < 130000:
		return 12
	elif 130000 <= time and time < 140000:
		return 13
	elif 140000 <= time and time < 150000:
		return 14
	elif 150000 <= time and time < 160000:
		return 15
	elif 160000 <= time and time < 170000:
		return 16
	elif 170000 <= time and time < 180000:
		return 17
	elif 180000 <= time and time < 190000:
		return 18
	elif 190000 <= time and time < 200000:
		return 19
	elif 200000 <= time and time < 210000:
		return 20
	elif 210000 <= time and time < 220000:
		return 21
	elif 220000 <= time and time < 230000:
		return 22
	else:
		return 23

def main():

	# road info
	roadNet = dict()
	read_road_info('map.txt', roadNet)

	for folder in os.listdir('point'):
		for file in os.listdir('point/'+folder):

			# track info
			timeList = list()
			read_track_info('point/'+folder+'/'+file, timeList)
			#print timeList
	
			# path info
			pathList = list()
			read_path_info('path/'+folder+'/'+file, pathList)

			# path length
			sum = 0
			for path in pathList:
				try:
					sum += float(roadNet[path])
				except KeyError:
					break
			if sum == 0:
				continue

			# time zones
			try:
				timeZone = time_zones(int(timeList[0]))
			except IndexError:
				continue

			# average speed
			time = trip_time_seconds(timeList)
			timeSpan = float(time) / 3600
			if timeSpan == 0:
				continue
			avr_speed = sum / timeSpan / 1000

			# save file
			record = ','.join([folder, repr(timeZone), repr(time), repr(sum), repr(avr_speed)])
			fw = open('time_zone/'+repr(timeZone)+'.txt', 'a')
			fw.writelines(record + '\n')

			print folder + ':' + file[:-4] + ' complete.'


if __name__ == '__main__':
	main()
