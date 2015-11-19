import numpy as np
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
def main():
    xIn, yIn = np.loadtxt('taxi.txt', delimiter=',', usecols=(4,5), unpack=True)
    print "The point number is:",len(xIn)
    length=len(xIn)
    for i in range(length):
        xIn[i],yIn[i]=transform(xIn[i],yIn[i])
        #if i%(length/10)==0:
        #    print i*10/length
    rst = np.column_stack((xIn, yIn))
    np.savetxt('rst.csv', rst, delimiter=",", fmt="%s")
    print ("Transformation completed.")

if __name__ == "__main__":
    main()

