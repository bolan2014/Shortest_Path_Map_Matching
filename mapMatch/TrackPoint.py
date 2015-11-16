class TrackPoint:
    def __init__(self, line):
        record = line.split(',')
        self.date = record[0]
        self.time = record[1]
	self.datetime = (record[0]+record[1])
        self.city = record[2]
        self.probeid = int(record[3])
        self.long = float(record[4])
        self.lat = float(record[5])
        self.speed = float(record[6])
        self.angle = int(record[7])
	self.flag = int(record[8])
	#self.datetime2 = record[9]
    def shortinfo(self):
        outline = "%5d,%15s,%11.6f,%10.6f\n"%(self.probeid, self.time, self.long, self.lat)
        return outline