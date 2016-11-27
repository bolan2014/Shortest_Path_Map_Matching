'''
Separate trips with passengers of each taxi.
'''

import sys
import os

def sprt(ifile):
	info = dict()
	order = 1
	fo = open(ifile, 'r')
	while True:
		line = fo.readline()
		if not line:
			break
		tmp = line.split(',')
		if tmp[8] == '1':
			if not info.has_key(order):
				info[order] = dict()
			info[order][tmp[1]] = tmp
		else:
			order += 1
	fo.close()
	return info

def sorted_dict(info):
	key = info.keys()
	key.sort()
	return map(info.get, key)

def get_trip(folder, info):
	count = 0
	for i in info.iterkeys():
		count += 1
		new_info = sorted_dict(info[i])
		fo = open('%s%s.txt'%(folder,count),'w')
		for j in new_info:
			fo.writelines(','.join(j))
		fo.close()

def main():
	for ifile in os.listdir('raw_gps/'):
		folder = 'section/'+ifile[0:5]+'/'
		info = sprt('raw_gps/'+ifile)
		get_trip(folder, info)
		print ifile[0:5] + ' complete.\n'
	
if __name__ == '__main__':
	main()
