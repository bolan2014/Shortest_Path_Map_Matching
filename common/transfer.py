from math import sqrt,sin,cos
import os
import sys
sys.path.append("..")
from mapMatch import TrackPoint

pwd = os.getcwd()+'/'

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
    ret=300.0+x+2.0*y+0.1*x*x+0.1*x*y+0.1*sqrt(abs(x))
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

def trans_trackInfo(rfile, wfile, tracklist, tracktime):
    fr = open(pwd+rfile, 'r')
    fw = open(pwd+wfile, 'w')
    for line in fr:
        tmp = line.split(',')
        x = float(tmp[4])
        y = float(tmp[5])
        x,y = transform(x, y) #caliberate gps points
        tmp[4] = str(x)
        tmp[5] = str(y)

        info = ",".join(tmp)
        fw.writelines(info + '\n')

        #get track info
        record = TrackPoint.TrackPoint(info)
        tracklist[record.datetime] = record
        tracktime.append(record.datetime)

    fr.close()
    fw.close()
