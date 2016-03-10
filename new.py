'''
GPS data processing
'''

import os
import sys
from mapMatch import read as r
from mapMatch import grid as g
from mapMatch import revise as rvs
from common import RemoveDuplicates
from common import transfer as t
from common import Dijkstra as Dj
from common import Geometry as G

REDUCTION_RATE = 0.01
REDUCE2 = 0.3
pwd = os.getcwd()

def main():

    #name = sys.argv[1]
    #print '\nInitializing...\n'

    linklist = dict()
    linkID = list()
    nodelist = dict()

    m_file = 'map.txt'

    #print 'Reading DRMLink info...'
    r.ReadingDRMinfo(m_file, linklist, linkID, nodelist)
    
    #print '\nCollecting links of Grid for type 1...'
    gridlink_1 = g.CollectGridLinks(1, linklist, linkID)

    #print '\nCollecting links of Grid for type 2...'
    gridlink_2 = g.CollectGridLinks(2, linklist, linkID)
    
    for folder in os.listdir('section'):
        #if int(folder) < int(name):
            #continue
        for t_file in os.listdir('section/'+folder):

            tracktime = list()
            tracklist = dict()
            w_file = 'gps/'+folder+'/'+t_file
            #print 'Tansfering gps data...\n'
            t.trans_trackInfo('section/'+folder+'/'+t_file, w_file, tracklist, tracktime)
            #print ("Transformation completed.\n")

            G1 = list()
            G2 = list()

            if not tracktime:
                continue

            i_start = 0
            while True:
                try:
                    itime = tracktime[i_start]
                    (x2, y2) = g.GetGridIndex(2, tracklist[itime].long, tracklist[itime].lat)
                    track_links = g.AdjacentGridLinks(2, x2, y2, gridlink_2)
                except IndexError:
                    break
                if track_links:
                    s_links = track_links
                    break
                else:
                    tracktime.remove(itime)
                i_start += 1
            i_end = len(tracktime)-1

            while True:
                try:
                    itime = tracktime[i_end]
                except IndexError:
                    break
                (x2, y2) = g.GetGridIndex(2, tracklist[itime].long, tracklist[itime].lat)
                try:
                    track_links = g.AdjacentGridLinks(2, x2, y2, gridlink_2)
                except IndexError:
                    break
                if track_links:
                    e_links = track_links
                    break
                else:
                    tracktime.remove(itime)
                i_end -= 1

            track_number = i_end-i_start+1    
            if track_number > 0:
                for itrack in range(i_start, i_end+1):
                    track_line = tracklist[tracktime[itrack]]
                    (x1, y1) = g.GetGridIndex(1, track_line.long, track_line.lat)
                    try:
                        G1 += g.AdjacentGridLinks(1, x1, y1, gridlink_1)
                        (x2, y2) = g.GetGridIndex(2, track_line.long, track_line.lat)
                        G2 += g.AdjacentGridLinks(2, x2, y2, gridlink_2)
                    except IndexError:
                        continue
            else:
                continue
            G1 = RemoveDuplicates.unique(G1)

            number_gps = {}
            for iid in G2:
                if number_gps.has_key(iid):
                    number_gps[iid] += 1
                else:
                    number_gps[iid] = 1

            G2 = RemoveDuplicates.unique(G2)

            G3 = list(set(G1) - set(G2))
            Gtrip = {}
            GLinkNode = {}
            GraphNet = []
            GraphNet_part = []
            Gpredecessor = []

            for iid in G3:
                ilink = linklist[iid]
                GraphNet.append(ilink.linkid)
                if ilink.regulation == 2:
                    g.AddLink(Gtrip, ilink.node1, ilink.node2, ilink.length)
                    g.AddLink(GLinkNode, ilink.node1, ilink.node2, ilink.linkid)
                elif ilink.regulation == 3:
                    g.AddLink(Gtrip, ilink.node2, ilink.node1, ilink.length)
                    g.AddLink(GLinkNode, ilink.node2, ilink.node1, ilink.linkid)
                else:
                    g.AddLink(Gtrip, ilink.node1, ilink.node2, ilink.length)
                    g.AddLink(Gtrip, ilink.node2, ilink.node1, ilink.length)
                    g.AddLink(GLinkNode, ilink.node1, ilink.node2, ilink.linkid)
                    g.AddLink(GLinkNode, ilink.node2, ilink.node1, ilink.linkid)

            for iid in G2:
                ilink = linklist[iid]
                GraphNet.append(ilink.linkid)
                if ilink.regulation == 2:
                    g.AddLink(Gtrip, ilink.node1, ilink.node2, ilink.length*REDUCTION_RATE*pow(REDUCE2,number_gps[iid]))
                    g.AddLink(GLinkNode, ilink.node1, ilink.node2, ilink.linkid)
                elif ilink.regulation == 3:
                    g.AddLink(Gtrip, ilink.node2, ilink.node1, ilink.length*REDUCTION_RATE*pow(REDUCE2,number_gps[iid]))
                    g.AddLink(GLinkNode, ilink.node2, ilink.node1, ilink.linkid)
                else:
                    g.AddLink(Gtrip, ilink.node1, ilink.node2, ilink.length*REDUCTION_RATE*pow(REDUCE2,number_gps[iid]))
                    g.AddLink(Gtrip, ilink.node2, ilink.node1, ilink.length*REDUCTION_RATE*pow(REDUCE2,number_gps[iid]))
                    g.AddLink(GLinkNode, ilink.node1, ilink.node2, ilink.linkid)
                    g.AddLink(GLinkNode, ilink.node2, ilink.node1, ilink.linkid)

            GraphNet = RemoveDuplicates.unique(GraphNet)
            s_links = RemoveDuplicates.unique(s_links)
            e_links = RemoveDuplicates.unique(e_links)
            s_links.sort()

            # print 'start links:', s_links
            # print 'end links:', e_links

            #print '\nFinding shortest path...'

            TRIP_FIRST_ID = 100
            TRIP_LAST_ID = 111

            number_trip = 1
            number_path = 0
            end_mod = dict()
            shortest_path = list()

            g.AddVirtualLinks(Gtrip, s_links, e_links, linklist, end_mod)

            if Gtrip and s_links and e_links:
                shortest_path = Dj.shortestPath(Gtrip, TRIP_FIRST_ID, TRIP_LAST_ID)
                if shortest_path:
                    shortest_path[0] = end_mod[shortest_path[0]][shortest_path[1]]
                    shortest_path[-1] = end_mod[shortest_path[-2]][shortest_path[-1]]
                    number_path += 1

                D, P = Dj.Dijkstra(Gtrip, TRIP_FIRST_ID, TRIP_LAST_ID)
                for key in P.keys():
                    if key != TRIP_LAST_ID and key != TRIP_LAST_ID:
                        key2 = P[key]
                        if key2 != TRIP_FIRST_ID and key2 != TRIP_LAST_ID:
                            Gpredecessor.append(GLinkNode[key2][key])
                # print shortest_path

            if shortest_path:
                try:
                    rvs.RevisePathEndpoints(tracklist, tracktime, linklist, GLinkNode, s_links, e_links, shortest_path)
                except KeyError:
                    continue
            ipa = 0
            pathlinks = list()
            rst_file = open('path/'+folder+'/'+t_file, 'w')
            pathnodes = shortest_path
            if pathnodes:
                while ipa <= len(pathnodes)-2:
                    try:
                        lid = GLinkNode[pathnodes[ipa]][pathnodes[ipa+1]]
                    except KeyError:
                        ipa += 1
                        continue
                    pathlinks.append(lid)
                    #ipa += 1
                for link in pathlinks:
                    rst_file.write(folder)
                    rst_file.write(',' + str(link) + '\n')
            else:
                rst_file.write(folder)
                rst_file.write(',' + '0' + '\n')
                rst_file.close()

            #print '\nAttaching points to road...' 
            rvs.point_on_road(tracktime, tracklist, pathlinks, linklist, folder+'/'+t_file)   
            print '\n'+folder+': '+t_file+' complete.'
              
if __name__ == "__main__":
    main()
