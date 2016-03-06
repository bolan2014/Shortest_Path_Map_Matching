'''
reading info of link, node, track
'''

import SHlink


def ReadingDRMinfo(fname, linklist, linkID, nodelist):
    fr = open(fname, 'r')

    for line in fr:
        link = SHlink.SHlink(line)
        linklist[link.linkid] = link
        linkID.append(link.linkid)

        nodelist[link.node1] = link
    fr.close()

''' global: nodelist linklist linkID tracktime tracklist '''
