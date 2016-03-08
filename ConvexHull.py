'''
Javis March
'''

import sys
import numpy as np

# Function to know if we have a CCW turn
def CCW(p1, p2, p3):
	if (p3[1]-p1[1])*(p2[0]-p1[0]) >= (p2[1]-p1[1])*(p3[0]-p1[0]):
		return True
	return False

# Main function:
def GiftWrapping(S):
	n = len(S)
	P = [None] * n
	l = np.where(S[:,0] == np.min(S[:,0]))
	pointOnHull = S[l[0][0]]
	i = 0
	while True:
		P[i] = pointOnHull
		P[i] = list(P[i]) #array to list
		endpoint = S[0]
		for j in range(1,n):
			if (endpoint[0] == pointOnHull[0] and endpoint[1] == pointOnHull[1]) or not CCW(S[j],P[i],endpoint):
				endpoint = S[j]
		i += 1
		pointOnHull = endpoint
		if endpoint[0] == P[0][0] and endpoint[1] == P[0][1]:
			break
	for i in range(n):
		if P[-1] == None:
			del P[-1]
	return P

''' Compute the polygonal area. '''

def GetAreaOfTri(a, b ,c):
	vec1 = [a[i]-b[i] for i in xrange(len(a))]
	vec2 = [b[i]-c[i] for i in xrange(len(b))]

	vec = [vec1, vec2]
	print abs(np.linalg.det(vec)/2)
	return abs(np.linalg.det(vec)/2)

def GetAreaOfCH(points):
	if len(points) < 3:
		Exception('at least 3 points')
	
	area = 0
	for i in range(len(points)-2):
		area +=GetAreaOfTri(points[0], points[1], points[2])
		del points[1]

	return area
'''
def main():
	points = [[-1,0], \
		[-1,1], \
	    [0,2], \
	    [1,1], \
	    [1,0]]

	print points
	res = GetAreaOfCH(points)
	print res
'''

def main():
	'''	try:
		N = int(sys.argv[1])
	except:
		N = int(input("Introduce N: "))
	'''	
	# By default we build a random set of N points with coordinates in [0,300)x[0,300):
	#P = np.array([(np.random.randint(0,300),np.random.randint(0,300)) for i in range(2)])
	ox,oy  = np.loadtxt('Sample.txt', delimiter=',', usecols=(1,2), unpack=True)
	P = np.column_stack((ox, oy))
	print len(P)
	points = GiftWrapping(P)
	print len(points)
	res = GetAreaOfCH(points)
	print res

if __name__ == '__main__':
  main()
