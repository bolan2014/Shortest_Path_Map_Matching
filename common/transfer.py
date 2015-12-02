from math import sqrt,sin,cos

#GPS point transforming process, only works in PRC.
pi=3.14159265358979324
a=6378245.0
ee=0.00669342162296594323

def transforlat(x,y):
    ret=-100.0+2.0*x+3.0*y+0.2*y*y+0.1*x*y+0.2*sqrt(abs(x))
    ret+=(20.0*sin(6.0*x*pi)+20.0*sin(2.0*x*pi))*2.0/3.0
    ret+=(20.0*sin(y*pi)+40.0*sin(y/3.0*pi))*2.0/3.0
    ret+=(160.0*sin(y/12.0*pi)+320.0*sin(y/30.0*pi))*2.0/3.0
    return ret

def transforlon(x,y):
    ret=300.0+x+2.0*y++0.1*x*x+0.1*x*y+0.1*sqrt(abs(x))
    ret+=(20.0*sin(6.0*x*pi)+20.0*sin(2.0*x*pi))*2.0/3.0
    ret+=(20.0*sin(x*pi)+40.0*sin(x/3.0*pi))*2.0/3.0
    ret+=(150.0*sin(x/12.0*pi)+300.0*sin(x/30.0*pi))*2.0/3.0
    return ret   

def transform(lon,lat):
    dlat=transforlat(lon-105.0,lat-35.0)
    dlon=transforlon(lon-105.0,lat-35.0)
    radlat=lat/180.0*pi
    magic=sin(radlat)
    magic=1-ee*magic*magic
    sqrtmagic=sqrt(magic)
    dlat=(dlat*180.0)/((a*(1-ee))/(magic*sqrtmagic)*pi)
    dlon=(dlon*180.0)/(a/sqrtmagic*cos(radlat)*pi)
    gcjlat=lat+dlat
    gcjlon=lon+dlon
    return gcjlon,gcjlat

#main process on txt
def readtxt(files):
    flink=open(files,'r')
    d=[]
    while 1:
        line=flink.readline() 
        if not line:
            break
        linesp=line.split(',')
        d.append(linesp)
    flink.close()
    return d

def writetxt(txt, files):
     flink=open(files,'w')
     for i in range(len(txt)):
         joinline=",".join(txt[i])
         flink.writelines(joinline)
     flink.close()

def trans(rfile, wfile):
    print 'Transfering gps data...'
    txt = readtxt(rfile)
    for i in range(len(txt)):
        xIn=float(txt[i][4])
        yIn=float(txt[i][5])
        xIn,yIn=transform(xIn,yIn)
        txt[i][4]=str(xIn)
        txt[i][5]=str(yIn)

    writetxt(txt, wfile)
    print ("Transformation completed.\n")
