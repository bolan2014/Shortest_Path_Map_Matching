'''
two kinds of grid.
'''
import sys
sys.path.append("..")
from common import Geometry as G

GRID_LONG_NUM_A = 50
GRID_LAT_NUM_A = 50

GRID_LONG_NUM_B = 500
GRID_LAT_NUM_B = 400

TRIP_FIRST_ID = 100
TRIP_LAST_ID = 111

def GetGridIndex(type, longi, lat):
    if type==1:
        gridnumlong=GRID_LONG_NUM_A
        gridnumlat=GRID_LAT_NUM_A
    elif type==2:
        gridnumlong=GRID_LONG_NUM_B
        gridnumlat=GRID_LAT_NUM_B
    (ori_longi, ori_lat) = (121.31, 31.08)
    x=(longi-ori_longi)/(1.0/8.0/gridnumlong)
    if x>=0:
        i_x = int(x)
    else:
        i_x=-1
    y=(lat-ori_lat)/(1.0/12.0/gridnumlat)
    if y>=0:
        i_y = int(y)
    else:
        i_y=-1

    return (i_x, i_y)

def GetPointGridxy(type, longi, lat):
    if type==1:
        gridnumlong=GRID_LONG_NUM_A
        gridnumlat=GRID_LAT_NUM_A
    elif type==2:
        gridnumlong=GRID_LONG_NUM_B
        gridnumlat=GRID_LAT_NUM_B
    
    (ori_longi, ori_lat) = (121.31, 31.08)
    x=(longi-ori_longi)/(1.0/8.0/gridnumlong)
    y=(lat-ori_lat)/(1.0/12.0/gridnumlat)

    return (x, y)

def CollectGridLinks(type, linklist, linkID):
    if type == 1:
        gridnumlong = GRID_LONG_NUM_A
        gridnumlat = GRID_LAT_NUM_A
    elif type == 2:
        gridnumlong = GRID_LONG_NUM_B
        gridnumlat = GRID_LAT_NUM_B

    grid = [[[] for i in range(3*gridnumlat)] for j in range(3*gridnumlong)]
    (ori_longi, ori_lat) = (121.31, 31.08)
    for ilink in linkID:
        if linklist[ilink].internumber>0:
            v = linklist[ilink].interlist
            counti = 0
            for n in range(linklist[ilink].internumber):
                (i, j) = GetGridIndex(type, v[n][0], v[n][1])
                if i>=3*gridnumlong or i<0 or j>=3*gridnumlat or j<0:
                    break
                counti += 1
            if counti==linklist[ilink].internumber:
                for n in range(1, counti):
                    (ip, jp) = GetGridIndex(type, v[n-1][0], v[n-1][1])		
                    if ilink not in grid[ip][jp]:
                        grid[i][j].append(ilink)
                    (i, j) = GetGridIndex(type, v[n][0], v[n][1])
                    
                    m1=abs(i-ip)
                    m2=abs(j-jp)
                    i_x=min(i,ip)
                    j_y=min(j,jp)             
                    if m1==0 and m2==0:
                        break
                    if m1==0 and m2>1:
                        for mj in range(m2):
                            if not ilink in grid[i][j_y+mj]:
                                grid[i][j_y+mj].append(ilink)
                    if m2==0 and m1>1:
                        for mi in range(m1):
                            if not ilink in grid[i_x+mi][j]:
                                grid[i_x+mi][j].append(ilink)
                    if m1>0 and m2>0:
                        A=G.Point()
                        B=G.Point()            
                        P1=G.Point()
                        P2=G.Point()
                        P3=G.Point()
                        P4=G.Point()
                        (A.x,A.y)= GetPointGridxy(type,v[n-1][0],v[n-1][1])
                        (B.x,B.y)= GetPointGridxy(type,v[n][0],v[n][1])              
                       
                        for  r1 in range(m1+1):
                            for r2 in range(m2+1):
                                 grid[i_x+r1][j_y+r2]
                                 P1.x=i_x+r1
                                 P1.y=j_y+r2
                                 P2.x=i_x+r1+1
                                 P2.y=j_y+r2
                                 P3.x=i_x+r1+1
                                 P3.y=j_y+r2+1
                                 P4.x=i_x+r1
                                 P4.y=j_y+r2+1
                                 if G.checkintersect(A,B,P1,P2,P3,P4)==1:
                                    if not ilink in grid[i_x+r1][j_y+r2]:
                                        grid[i_x+r1][j_y+r2].append(ilink)
                    ip=i
                    jp=j
        else:
            meshnode=linklist[ilink].node1 
            x=nodelist[meshnode].long     
            y=nodelist[meshnode].lat  
            (i, j)=GetGridIndex(type,x,y)
            if i>=5*gridnumlong or i<0 or j>=5*gridnumlat or j<0:
                continue           
            if not ilink in grid[i][j]:
                grid[i][j].append(ilink)
            
    return grid

def AddLink( g, u, v, w ):
    if g.has_key(u):
        g[u][v] = w
    else:
        g[u] = {v:w}

def AddVirtualLinks(net, s_candidate, e_candidate, linklist, end_mod):
    for i_id in s_candidate:
        ilink = linklist[i_id]
        if ilink.getregulation() == 2:
            AddLink(net, TRIP_FIRST_ID, ilink.node2, 0.0)
            AddLink(end_mod, TRIP_FIRST_ID, ilink.node2, ilink.node1)
        elif ilink.getregulation() == 3:
            AddLink(net, TRIP_FIRST_ID, ilink.node1, 0.0)
            AddLink(end_mod, TRIP_FIRST_ID, ilink.node1, ilink.node2)
        else:
            AddLink(net, TRIP_FIRST_ID, ilink.node2, 0.0)
            AddLink(end_mod, TRIP_FIRST_ID, ilink.node2, ilink.node1)
            AddLink(net, TRIP_FIRST_ID, ilink.node1, 0.0)
            AddLink(end_mod, TRIP_FIRST_ID, ilink.node1, ilink.node2)

    for i_id in e_candidate:
        ilink = linklist[i_id]
        if ilink.getregulation() == 2:
            AddLink(net, ilink.node1, TRIP_LAST_ID, 0.0)
            AddLink(end_mod, ilink.node1, TRIP_LAST_ID, ilink.node2)
        elif ilink.getregulation() == 3:
            AddLink(net, ilink.node2, TRIP_LAST_ID, 0.0)
            AddLink(end_mod, ilink.node2, TRIP_LAST_ID, ilink.node1)
        else:
            AddLink(net, ilink.node1, TRIP_LAST_ID, 0.0)
            AddLink(end_mod, ilink.node1, TRIP_LAST_ID, ilink.node2)
            AddLink(net, ilink.node2, TRIP_LAST_ID, 0.0)
            AddLink(end_mod, ilink.node2, TRIP_LAST_ID, ilink.node1)

def AdjacentGridLinks(type, x ,y, gridlink_):
    if type==1:
        gridnumlong=GRID_LONG_NUM_A
        gridnumlat=GRID_LAT_NUM_A
    elif type==2:
        gridnumlong=GRID_LONG_NUM_B
        gridnumlat=GRID_LAT_NUM_B    

    gridlink=gridlink_
    glinks=[]
    
    if x==0:
      if y==0:
         glinks=glinks+gridlink[x][y]
         glinks=glinks+gridlink[x+1][y]
         glinks=glinks+gridlink[x+1][y+1]
         glinks=glinks+gridlink[x][y+1]
      elif y==5*gridnumlat-1:
         glinks=glinks+gridlink[x][y]
         glinks=glinks+gridlink[x][y-1]
         glinks=glinks+gridlink[x+1][y-1]
         glinks=glinks+gridlink[x+1][y]
      else:
         glinks=glinks+gridlink[x][y]
         glinks=glinks+gridlink[x][y-1]
         glinks=glinks+gridlink[x+1][y-1]
         glinks=glinks+gridlink[x+1][y]
         glinks=glinks+gridlink[x+1][y+1]
         glinks=glinks+gridlink[x][y+1]
    elif x==5*gridnumlong-1:
      if y==0:
         glinks=glinks+gridlink[x][y]
         glinks=glinks+gridlink[x][y+1]
         glinks=glinks+gridlink[x-1][y+1]
         glinks=glinks+gridlink[x-1][y]
      elif y==5*gridnumlat-1:
         glinks=glinks+gridlink[x][y]
         glinks=glinks+gridlink[x-1][y]
         glinks=glinks+gridlink[x-1][y-1]
         glinks=glinks+gridlink[x][y-1]
      else:
         glinks=glinks+gridlink[x][y]
         glinks=glinks+gridlink[x][y+1]
         glinks=glinks+gridlink[x-1][y+1]
         glinks=glinks+gridlink[x-1][y]
         glinks=glinks+gridlink[x-1][y-1]
         glinks=glinks+gridlink[x][y-1]
    else:
      if y==0:
         glinks=glinks+gridlink[x][y]
         glinks=glinks+gridlink[x+1][y]
         glinks=glinks+gridlink[x+1][y+1]
         glinks=glinks+gridlink[x][y+1]
         glinks=glinks+gridlink[x-1][y+1]
         glinks=glinks+gridlink[x-1][y]
      elif y==5*gridnumlat-1:
         glinks=glinks+gridlink[x][y]
         glinks=glinks+gridlink[x-1][y]
         glinks=glinks+gridlink[x-1][y-1]
         glinks=glinks+gridlink[x][y-1]
         glinks=glinks+gridlink[x+1][y-1]
         glinks=glinks+gridlink[x+1][y]
      else:
         glinks=glinks+gridlink[x][y]
         glinks=glinks+gridlink[x-1][y]
         glinks=glinks+gridlink[x-1][y-1]
         glinks=glinks+gridlink[x][y-1]
         glinks=glinks+gridlink[x+1][y-1]
         glinks=glinks+gridlink[x+1][y]
         glinks=glinks+gridlink[x+1][y+1]
         glinks=glinks+gridlink[x][y+1]
         glinks=glinks+gridlink[x-1][y+1]
    return glinks 
