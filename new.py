'''
GPS data processing
'''

import os
from mapMatch import read
from mapMatch import grid
from common import RemoveDuplicates
def main():

    linklist = {}
    linkID = []
    nodelist = {}

    #m_file = os.getcwd() + '/ins.txt'

    #read.ReadingDRMlink(linklist, linkID, fname)
    #read.ReadingDRMnode(nodelist, fname)

    #link1 = grid.CollectGridLinks(1, linklist, linkID)
    #link2 = grid.CollectGridLinks(2, linklist, linkID)

    #print nodelist.keys()
    #print link1
    #print linklist.keys()

    
    tracktime = []
    tracklist = {}
    t_file = os.getcwd() + '/taxi.txt'
    read.ReadingTrackInfo(tracklist, tracktime, t_file)

    G1 = []
    G2 = []
    shortest_path = []

    i_start = 0
    while True:
        itime = tracktime[i_start]
        (x2, y2) = GetGridIndex(2, tracklist[itime].long, tracklist[itime].lat)
        track_links = AdjacentGridLinks(2, x2, y2)
        if track_links:
            s_links = track_links
            break
        else:
            tracktime.remove(itime)
        i_start += 1
    i_end = len(tracktime)-1

    while True:
        itime = tracktime[i_end]
        (x2, y2) = GetGridIndex(2, tracklist[itime].long, tracklist[itime].lat)
        track_links = AdjacentGridLinks(2, x2, y2)
        if track_links:
            e_links = track_links
            break
        else:
            tracktime.remove(itime)
        i_end -= 1

    track_number = i_end-i_start+1    
    if track_number >= 0:
        for itrack in range(i_start, i_end+1)
            track_line = tracklist[tracktime[itrack]]
            (x1, y1) = GetGridIndex(1, track_line.long, track_line.lat)
            G1 += AdjacentGridLinks(1, x1, y1)
            (x2, y2) = GetGridIndex(2, track_line.long, track_line.lat)
            G2 += AdjacentGridLinks(2, x1, y1)

    G1 = RemoveDuplicates.unique(G1)
    

    print tracklist.keys()


if __name__ == "__main__":
    main()
