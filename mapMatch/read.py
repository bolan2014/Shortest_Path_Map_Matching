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
