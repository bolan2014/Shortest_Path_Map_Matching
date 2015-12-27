import shapefile
import numpy as np

def readtxt(files):
    data=np.loadtxt(files, delimiter=',')
    d=[]
    for i in data:
        d.append(int(i[1]))
    return d

def filtershp(shpname,filterlink):
    sf=shapefile.Reader(shpname)
    records=sf.records()
    length=len(records)
    print "\nThe length of the shp is: "+str(length)
    fullindex=range(length)
    for j in range(length-1,-1,-1):
        for i in filterlink:
            if records[j][0]==i:
                fullindex.pop(j)
    fullindex.sort(reverse=True)
    print '\nFiltershp finished. Waiting for editing...'
    w=shapefile.Editor(shpname)
    for i in fullindex:
        w.delete(i)
    w.save('Roadx.shp')
    print '\nCompleted.'

def main():
    print '\nSave the trip of taxi into shp file...'
    filterlink = readtxt('rst.csv')
    filterindex = filtershp('Road/Road.shp', filterlink)

#layer = iface.addVectorLayer("E:\ligroup\FCD\ShanghaiGIS\Roadx.shp", "Roadx", "ogr")

if __name__ == "__main__":
    main()
