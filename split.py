def readtxt(files):
    flink=open(files,'r')
    d={}
    query=[]
    while 1:
        line=flink.readline() 
        if not line:
            break
        linesp=line.split(',')
        if linesp[3] not in query:
            d[linesp[3]]={}
            query.append(linesp[3])
        d[linesp[3]][linesp[1]]=linesp
    flink.close()
    print files,'read'
    return d
data=readtxt('20110401.txt')

def sorteddict(dict1):
    key=dict1.keys()
    key.sort()
    return map(dict1.get,key)

def writetxt(files,d):
    for i in d.iterkeys():
        sortdi=sorteddict(d[i])
        flink=open('%s%s.txt'%(files,i),'w')
        for j in sortdi:
            flink.writelines(','.join(j))
        flink.close()
writetxt('raw_gps/',data)
