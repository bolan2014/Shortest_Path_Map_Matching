import tarfile
import os
import time
import shutil

from pyproj import Proj, transform
import numpy as np

def decompressiontar(sourcepath, despath):
	tar = tarfile.open(sourcepath)
	names = tar.getnames()
	for name in names:
		tar.extract(name, path = despath)
	tar.close()

def buildlist(sourcepath_name):
    with open(sourcepath_name, "r") as f:
        line = f.readline()
        columns = []
        while True:
            line = f.readline()
            if not line:
                f.close()
                return columns
            columns.append(line.split(','))

# transform from epsg 4326 to 3785
def trans(x, y):
	epsg4326 = Proj(proj='utm', zone=50, ellps='WGS84')
	epsg3785 = Proj(init = 'epsg:3785')
	x1, y1 = epsg4326(x, y)
	x2, y2 = transform(epsg4326, epsg3785, x1, y1)
	return x2, y2

def main():

    x, y = np.loadtxt('ins.txt', delimiter=',', usecols=(4,5), unpack=True)

    # epsg4236to3785(x, y)

    for i in range(len(x)):
        x[i], y[i] = trans(x[i], y[i])

    rst = np.column_stack((x, y))
    # print rst

    np.savetxt('rst.csv', rst, delimiter=",", fmt="%s")
    print ("Transformation completed.")

if __name__ == '__main__':
	#start = time.time()
	main()
	#end = time.time()
	#print(end - start)
