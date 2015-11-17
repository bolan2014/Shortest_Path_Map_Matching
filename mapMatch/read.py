'''
reading info of link and node
'''

import SHlink

def ReadingDRMlink():
    print '\treading DRMlink ...'
    fl = open('filename', 'r')
    
    while 1:
        line = fl.readline()
        if not line:
            break
        link = SHlink.SHlink(line)
        linklist[link.linkid] = link
        linkID.append(link.linkid)

    fl.close()

def ReadingDRMnode():
    print '\treading DRMnode ...'
    fn = open('filename', 'r')

    while 1:
        line = fn.readline()
        if not line:
            break
        node = SHlink.SHlink(line)
        nodelist[node.node1] = node

    fn.close()

def ReadingTrackInfo():
    ft = open('filename', 'r')

    while 1:
        line = ft.readline()
        if not line:
            break;
        record = TrackPoint.TrackPoint(line)
        tracklist[record.datetime] = record
        tracktime.append(record.datetime)

    ft.close()
''' global: nodelist linklist tracktime tracklist '''
