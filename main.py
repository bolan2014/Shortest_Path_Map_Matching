linklist={}   #所有link的字典结构
linkID=[]     #所有linkid
nodelist={}   #所有node的字典结构

print 'Initializing...'
print 'Reading DRMLink into linklist and linkID...'
ReadingDRMLink()

print 'Reading DRMNode into nodelist...'
ReadingDRMNode()

print '\tCollecting links of Grid for type 1...'
gridlink_1 = CollectGridLinks(1)
print '\tCollecting links of Grid for type 2...'
gridlink_2 = CollectGridLinks(2)

print '------ Start ------'
number_trip=0  #统计trip数
number_path=0  #统计得到最短路径的trip数

VEHICLE_DIR='E:\\ligroup\\FCD\\MapMatchTest\\Sample2000000\\'
MMRESULT_DIR='E:\\ligroup\\FCD\\MapMatchTest\\MMResult -2\\'
file_tripidlist=open(MMRESULT_DIR+'TripIDList_Trip7-10amInzone\\'+'tripidlist.txt','w')

dirs=os.listdir(VEHICLE_DIR)
for idir in dirs:
    triplink=VEHICLE_DIR+idir+'\\'
    files=os.listdir(triplink)
    
    if not os.path.isdir(MMRESULT_DIR+'MMResult_Trip7-10amInzone\\'+idir):
        os.makedirs(MMRESULT_DIR+'MMResult_Trip7-10amInzone\\'+idir)
    mmresult_vehicle_dir=MMRESULT_DIR+'MMResult_Trip7-10amInzone\\'+idir
  
    if not os.path.isdir(MMRESULT_DIR+'MMGraphNet_Trip7-10amInzone\\'+idir):
        os.makedirs(MMRESULT_DIR+'MMGraphNet_Trip7-10amInzone\\'+idir)
    MMGraphNet_vehicle_dir=MMRESULT_DIR+'MMGraphNet_Trip7-10amInzone\\'+idir
    
    if not os.path.isdir(MMRESULT_DIR+'MMPredecessor_Trip7-10amInzone\\'+idir):
        os.makedirs(MMRESULT_DIR+'MMPredecessor_Trip7-10amInzone\\'+idir)
    MMPredecessor_vehicle_dir=MMRESULT_DIR+'MMPredecessor_Trip7-10amInzone\\'+idir
    
    if not os.path.isdir(MMRESULT_DIR+'MMtravelTime\\'+idir):
        os.makedirs(MMRESULT_DIR+'MMtravelTime\\'+idir)
    MMTravelTime_vehicle_dir=MMRESULT_DIR+'MMtravelTime\\'+idir
    
    for ifile in files:
        G1=[]
        G2=[]
        shortest_path=[]
        
        #读trip文件
        trackdatetime=[]
        tracklist={}
        flink = open(VEHICLE_DIR+idir+'\\'+ifile,'r')
        while 1:
            line = flink.readline()
            if not line:
                break
            triprecord = TrackPoint1.TrackPoint(line)
            tracklist[triprecord.datetime]=triprecord
            trackdatetime.append(triprecord.datetime)
        flink.close()
        
        #如果trip文件为空，则结束当前trip的地图匹配，进入下一个trip
        if not tracklist:
            continue
        
        i_start=0
        while 1:
            idatetime=trackdatetime[i_start]
            (x2,y2)=GetGridIndex(2,tracklist[idatetime].long,tracklist[idatetime].lat)
            track_links=AdjacentGridLinks(2,x2,y2)
            if track_links:
                s_links=track_links
                break
            else:
                trackdatetime.remove(idatetime)
            i_start=i_start+1       
        
        i_end=len(trackdatetime)-1
        while 1:
            idatetime=trackdatetime[i_end]
            (x2,y2)=GetGridIndex(2,tracklist[idatetime].long,tracklist[idatetime].lat)
            track_links=AdjacentGridLinks(2,x2,y2)
            if track_links:
                e_links=track_links
                break
            else:
                trackdatetime.remove(idatetime)
            i_end=i_end-1
            
            
        track_number=i_end-i_start+1 #除去首尾没有候选link的trackpoint点之后，trip剩余轨迹点数量
        if track_number>=0:
            for itrack in range(i_start,i_end+1):
                track_line=tracklist[trackdatetime[itrack]]
                (x1,y1)=GetGridIndex(1,track_line.long,track_line.lat)
                G1=G1+AdjacentGridLinks(1,x1,y1)
                (x2,y2)=GetGridIndex(2,track_line.long,track_line.lat)
                G2=G2+AdjacentGridLinks(2,x2,y2) 
        
        G1=RemoveDuplicates.unique(G1)#trip经过点所有相邻的link
        
        #统计与link相邻的GPS点的数目
        number_gps={}
        for iid in G2:
            if number_gps.has_key(iid):
                number_gps[iid]=number_gps[iid]+1
            else:
                number_gps[iid]=1
        
        G2=RemoveDuplicates.unique(G2)#trip经过点最近的相邻的link
        #把除去trip经过点相邻link之外的link放入字结构的图中
        G3=list(set(G1)-set(G2))
        Gtrip={}
        GLinkNode={}
        GraphNet=[]
        GraphNet_part=[]         
        Gpredecessor=[]   
        #print G3     
        #print G3     
        for iid in G3:
            ilink = linklist[iid]
            GraphNet.append(ilink.linkid)
            if ilink.regulation == 2:
                AddLink(Gtrip, ilink.node1,ilink.node2,ilink.length)
                AddLink(GLinkNode, ilink.node1,ilink.node2,ilink.linkid)
                
            elif ilink.regulation == 3:
                AddLink(Gtrip, ilink.node2,ilink.node1,ilink.length)
                AddLink(GLinkNode, ilink.node2,ilink.node1,ilink.linkid)
            else:
                AddLink(Gtrip, ilink.node1,ilink.node2,ilink.length)
                AddLink(Gtrip, ilink.node2,ilink.node1,ilink.length) 
                AddLink(GLinkNode, ilink.node1,ilink.node2,ilink.linkid)
                AddLink(GLinkNode, ilink.node2,ilink.node1,ilink.linkid)           
        #把trip经过点相邻的link的长度缩小后，放入字结构的图中
        for iid in G2:
            ilink = linklist[iid]
            GraphNet.append(ilink.linkid)
            if ilink.regulation == 2:
                AddLink(Gtrip, ilink.node1,ilink.node2,ilink.length*REDUCTION_RATE*pow(REDUCE2,number_gps[iid]))
                AddLink(GLinkNode, ilink.node1,ilink.node2,ilink.linkid)
            elif ilink.regulation == 3:
                AddLink(Gtrip, ilink.node2,ilink.node1,ilink.length*REDUCTION_RATE*pow(REDUCE2,number_gps[iid]))
                AddLink(GLinkNode, ilink.node2,ilink.node1,ilink.linkid)
            else:
                AddLink(Gtrip, ilink.node1,ilink.node2,ilink.length*REDUCTION_RATE*pow(REDUCE2,number_gps[iid]))
                AddLink(Gtrip, ilink.node2,ilink.node1,ilink.length*REDUCTION_RATE*pow(REDUCE2,number_gps[iid]))
                AddLink(GLinkNode, ilink.node1,ilink.node2,ilink.linkid)
                AddLink(GLinkNode, ilink.node2,ilink.node1,ilink.linkid)

        GraphNet=RemoveDuplicates.unique(GraphNet)
        s_links=RemoveDuplicates.unique(s_links)
        e_links=RemoveDuplicates.unique(e_links)
        s_links.sort()
        print 'start links:',s_links
        print 'end links:',e_links
        
        #为起止点添加虚拟link
        end_mod = {}       
        AddVirtualLinks(Gtrip,s_links,e_links)
        
        ###寻找最短路径     
        print '\t\t Find shortest path...'
        print 'ifile',ifile
        number_trip=number_trip+1  
        print 'number_trip',number_trip
        if Gtrip and s_links and e_links:
            shortest_path = shortestPath(Gtrip, TRIP_FIRST_ID, TRIP_LAST_ID)
            if shortest_path:
                shortest_path[0] = end_mod[shortest_path[0]][shortest_path[1]]
                shortest_path[-1] = end_mod[shortest_path[-2]][shortest_path[-1]]
                number_path=number_path+1
                print 'number_path',number_path
            #找最短路径树    
            D,P = Dijkstra(Gtrip,TRIP_FIRST_ID,TRIP_LAST_ID)
            for key in P.keys():
                if key != TRIP_FIRST_ID and key != TRIP_LAST_ID:
                    key2=P[key]
                    if key2 != TRIP_FIRST_ID and key2 != TRIP_LAST_ID:
                        Gpredecessor.append(GLinkNode[key2][key])
            #print 'Shortest path:', shortest_path
            
        mmpathnodes=shortest_path  #用node集表示的匹配路径
        ###修正路径的起止点
        #print 'mmpathnodesold:',mmpathnodes  #修正前最短路径
        if mmpathnodes:
            RevisePathEndpoints()
        #print 'mmpathnodesnew:',mmpathnodes  #修正后最短路径,即匹配路径
          
        ###把最短路径转化为用link集表示的形式，并输出 
        ipa=0
        mmpathlinks=[]          
        mmresult_filename=mmresult_vehicle_dir+'\\'+"%s"%ifile
        mmresult_file=open(mmresult_filename,'w')            
        if mmpathnodes:
            #转化最短路径的node集为link集
            while ipa<=len(mmpathnodes)-2:
                #print mmpathnodes[i],mmpathnodes[i+1]
                MMlinkid=GLinkNode[mmpathnodes[ipa]][mmpathnodes[ipa+1]]
                mmpathlinks.append(MMlinkid)
                ipa+=1
            #输出link集
            for immlink in mmpathlinks:
                mmresult_file.write(ifile[:-4]) 
                mmresult_file.write(','+str(immlink)+'\n')
        else:  
            mmresult_file.write(ifile[:-4]) 
            mmresult_file.write(','+'0'+'\n')
        mmresult_file.close()
        
        ###输出最短路径树
        mmpredecessor_filename=MMPredecessor_vehicle_dir+'\\'+"%s"%ifile
        mmpredecessor_file=open(mmpredecessor_filename,'w') 
        if Gpredecessor:
            for plink in Gpredecessor:
                mmpredecessor_file.write(ifile[:-4])
                mmpredecessor_file.write(','+str(plink)+'\n')
        else:
            mmpredecessor_file.write(ifile[:-4])
            mmpredecessor_file.write(','+'0'+'\n')
        
        ###输出候选link网路
        mmgraph_filename=MMGraphNet_vehicle_dir+'\\'+"%s"%ifile
        mmgraph_file=open(mmgraph_filename,'w')
        GraphNet_part=list(set(GraphNet)-set(mmpathlinks)) #候选路网中，除去最短路径上links剩下的links
        if GraphNet_part:
            for glink in GraphNet_part:
                mmgraph_file.write(ifile[:-4])
                mmgraph_file.write(','+str(glink)+'\n')
        else:
            mmgraph_file.write(ifile[:-4] )
            mmgraph_file.write(','+'0'+'\n')  
            
        ###输出所有非空tripid
        file_tripidlist.write(str(number_trip)+','+ifile[:-4]+'\n')
             
        ###如果mmpathnodes为空，则结束当前trip的地图匹配，进入下一个trip     
        if not mmpathnodes:
            continue 

file_tripidlist.close()