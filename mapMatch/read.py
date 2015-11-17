'''
reading info of link, node, track
'''

import SHlink
import TrackPoint

def ReadingDRMlink(linklist, linkID, filename):
    fl = open(filename, 'r')
    
    while 1:
        line = fl.readline()
        if not line:
            break
        link = SHlink.SHlink(line)
        linklist[link.linkid] = link
        linkID.append(link.linkid)

    fl.close()

def ReadingDRMnode(nodelist, filename):
    fn = open(filename, 'r')

    while 1:
        line = fn.readline()
        if not line:
            break
        node = SHlink.SHlink(line)
        nodelist[node.node1] = node

    fn.close()

def ReadingTrackInfo(tracklist, tracktime, filename):
    ft = open(filename, 'r')

    while 1:
        line = ft.readline()
        if not line:
            break;
        record = TrackPoint.TrackPoint(line)
        tracklist[record.datetime] = record
        tracktime.append(record.datetime)

    ft.close()

''' global: nodelist linklist linkID tracktime tracklist '''