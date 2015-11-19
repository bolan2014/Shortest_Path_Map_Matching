'''
reading info of link, node, track
'''

import SHlink
import TrackPoint

def ReadingDRMlink(linklist, linkID, fname):
    fl = open(fname, 'r')
    
    while True:
        line = fl.readline()
        if not line:
            break
        link = SHlink.SHlink(line)
        linklist[link.linkid] = link
        linkID.append(link.linkid)

    fl.close()

def ReadingDRMnode(nodelist, fname):
    fn = open(fname, 'r')

    while True:
        line = fn.readline()
        if not line:
            break
        node = SHlink.SHlink(line)
        nodelist[node.node1] = node

    fn.close()

def ReadingTrackInfo(tracklist, tracktime, fname):
    ft = open(fname, 'r')

    while True:
        line = ft.readline()
        if not line:
            break;
        record = TrackPoint.TrackPoint(line)
        tracklist[record.datetime] = record
        tracktime.append(record.datetime)

    ft.close()

''' global: nodelist linklist linkID tracktime tracklist '''
