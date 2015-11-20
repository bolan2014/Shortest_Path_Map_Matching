#! /usr/bin/env python
#coding=utf-8
from math import sqrt

#点类
class Point:
    def __init__(self,xp=0.0,yp=0.0):
        self.x = xp
        self.y = yp

#判断点是否在线段上
#设点为Q，线段为P1P2 ，判断点Q在该线段上的依据是：( Q - P1 ) × ( P2 - P1 ) = 0 且 Q 在以 P1，P2为对角顶点的矩形内。
#前者保证Q点在直线P1P2上，后者是保证Q点不在线段P1P2的延长线或反向延长线上 
def checkpointonline(Q,p1,p2):
    if (p2.x-p1.x)*(Q.y-p1.y)-(p2.y-p1.y)*(Q.x-p1.x)<=1.0e-05 and \
        min(p1.x,p2.x)<=Q.x<=max(p1.x,p2.x) and min(p1.y,p2.y)<=Q.y<=max(p1.y,p2.y):
        return 1
    else:
        return 0

# 计算两点之间欧氏距离
def dist(p1, p2):
    return sqrt((p1.x-p2.x)**2+(p1.y-p2.y)**2)


#返回Mesh的左下角经纬度
def GetMeshOrigin(meshid):
    m1 = int(meshid/10000)
    m2 = int((meshid - m1*10000)/100)
    m3 = int((meshid - m1*10000 - m2*100)/10)
    m4 = int(meshid - m1*10000 - m2*100 - m3*10)
    lat = m1 * (2.0/3.0) + m3/12.0
    longi = m2 + 100.0 + m4/8.0
    return (longi, lat)
# (o_long,o_lat)=GetMeshOrigin(523646)
# o_long=136.75,o_lat=35.0

#下面两个函数实现经纬度坐标与自定义坐标之间的转换
#变换坐标
def lnglattoxy(p):
    #以mesh523646的左下角点做坐标原点
    p.x=(p.x - 121.31) * 91.0237947885214 * 1000.0
    p.y=(p.y - 31.08) * 111.11999965975954 * 1000.0
    return p

def xytolnglat(p):
    p.x= p.x/(91.0237947885214 * 1000.0) + 121.31
    p.y= p.y/(111.11999965975954 * 1000.0) + 31.08
    return p 
#计算两点之间在地球上的距离，以mesh523646左下角点为坐标原点
def geodist(Q1,Q2):
    P1=Point()
    P2=Point()
    P1.x=Q1.x
    P1.y=Q1.y
    P2.x=Q2.x
    P2.y=Q2.y
    P1=lnglattoxy(P1)
    P2=lnglattoxy(P2)
    d=dist(P1,P2)
    return d

#判断矩阵是否在线段两侧，如果是，则线段与矩阵相交,返回1，否则返回0
#矩阵四个顶点P1(x1,y1),P2(x2,y2),P3(x3,y3),P4(x4,y4)
#线段AB，A(a1,b1),B(a2,b2)
def checkintersect(A,B,P1,P2,P3,P4):
     a1=A.x
     b1=A.y
     a2=B.x
     b2=B.y
     x1=P1.x
     y1=P1.y
     x2=P2.x
     y2=P2.y
     x3=P3.x
     y3=P3.y
     x4=P4.x
     y4=P4.y
    
     t1=(y1-b1)*(a2-a1)-(x1-a1)*(b2-b1)
     t2=(y2-b1)*(a2-a1)-(x2-a1)*(b2-b1)
     t3=(y3-b1)*(a2-a1)-(x3-a1)*(b2-b1)
     t4=(y4-b1)*(a2-a1)-(x4-a1)*(b2-b1) 
     if t1>0 and t2>0 and t3>0 and t4>0:
         return 0
     if t1<0 and t2<0 and t3<0 and t4<0:
         return 0
     return 1
