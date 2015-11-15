'''
resolve the content of link
'''

class SHlink:
    def __init__(self, line):
        record = line.split(',')
        self.linkid = int(record[0])
        self.fc = int(record[1])
        self.length = float(record[2])
        self.node1 = int(record[3])                      
        self.node2 = int(record[4])                                    
        self.regulation = int(record[5])              
        self.fw = int(record[6])                     
        self.struct = int(record[7])                     
	self.internumber = int(record[8])
	if self.internumber < 0:
            self.internumber = 0
            
        self.interlist = []
    
        for i in range(self.internumber):
            longi = float(record[9 + 2*i])
            lat = float(record[9 + 2*i + 1])
            longilat = (longi, lat)
            
            self.interlist.append(longilat)
		
    def getregulation(self):
        return self.regulation
