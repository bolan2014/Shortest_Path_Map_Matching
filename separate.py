import sys

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
	for i in info.iterkeys():
		new_info = sorted_dict(info[i])
		fo = open('%s%s.txt'%(folder,i),'w')
		for j in new_info:
			fo.writelines(','.join(j))
		fo.close()

def main():
	ifile = sys.argv[1]
	folder = sys.argv[2]
	info = sprt(ifile)
	get_trip(folder, info)
	
if __name__ == '__main__':
	main()
