'''
Split raw GPS data by taxi ID.
'''

import sys

def readtxt(files):
    flink = open(files,'r')
    d = dict()
    query = list()
    while True:
        line = flink.readline() 
        if not line:
            break
        linesp = line.split(',')
        if linesp[3] not in query:
            d[linesp[3]] = dict()
            query.append(linesp[3])
        d[linesp[3]][linesp[1]] = linesp
    flink.close()
    print files, 'read'
    return d

def sorteddict(dict1):
    key = dict1.keys()
    key.sort()
    return map(dict1.get, key)

def writetxt(files,d):
    for i in d.iterkeys():
        sortdi = sorteddict(d[i])
        flink = open('%s%s.txt'%(files,i), 'w')
        for j in sortdi:
            flink.writelines(','.join(j))
        flink.close()

if __name__ == '__main__':
    data = readtxt(sys.argv[1])
    writetxt('raw_gps/', data)

