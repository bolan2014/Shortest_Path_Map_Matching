#coding=utf-8
# Dijkstra's algorithm for shortest paths
# David Eppstein, UC Irvine, 4 April 2002
# 注：此程序David Eppstein的原始程序有所修改
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117228
from PrioDict import priorityDictionary

def Dijkstra(G,start,end=None):
	"""
	Find shortest paths from the start vertex to all
	vertices nearer than or equal to the end.

	The input graph G is assumed to have the following
	representation: A vertex can be any object that can
	be used as an index into a dictionary.  G is a
	dictionary, indexed by vertices.  For any vertex v,
	G[v] is itself a dictionary, indexed by the neighbors
	of v.  For any edge v->w, G[v][w] is the length of
	the edge.  This is related to the representation in
	<http://www.python.org/doc/essays/graphs.html>
	where Guido van Rossum suggests representing graphs
	as dictionaries mapping vertices to lists of neighbors,
	however dictionaries of edges have many advantages
	over lists: they can store extra information (here,
	the lengths), they support fast existence tests,
	and they allow easy modification of the graph by edge
	insertion and removal.  Such modifications are not
	needed here but are important in other graph algorithms.
	Since dictionaries obey iterator protocol, a graph
	represented as described here could be handed without
	modification to an algorithm using Guido's representation.

	Of course, G and G[v] need not be Python dict objects;
	they can be any other object that obeys dict protocol,
	for instance a wrapper in which vertices are URLs
	and a call to G[v] loads the web page and finds its links.
	
	The output is a pair (D,P) where D[v] is the distance
	from start to v and P[v] is the predecessor of v along
	the shortest path from s to v.
	
	Dijkstra's algorithm is only guaranteed to work correctly
	when all edge lengths are positive. This code does not
	verify this property for all edges (only the edges seen
	before the end vertex is reached), but will correctly
	compute shortest paths even for some graphs with negative
	edges, and will raise an exception if it discovers that
	a negative edge has caused it to make a mistake.
	"""

	D = {}	# dictionary of final distances
	P = {}	# dictionary of predecessors
	Q = priorityDictionary()   # est.dist. of non-final vert.
	Q[start] = 0
	
	for v in Q:
		D[v] = Q[v]
		if v == end: break
		# 避免断头路
		if G.has_key(v):
			for w in G[v]:
				vwLength = D[v] + G[v][w]
				if w in D:
					if vwLength < D[w]:
						raise ValueError, "Dijkstra: found better path to already-final vertex"
				elif w not in Q or vwLength < Q[w]:
					Q[w] = vwLength
					P[w] = v
	
	return (D,P)



def shortestPath(G,start,end):
	"""
	Find a single shortest path from the given start vertex
	to the given end vertex.
	The input has the same conventions as Dijkstra().
	The output is a list of the vertices in order along
	the shortest path.
	"""

	D,P = Dijkstra(G,start,end)
#	flog1 = open('flog1.txt', 'w')
#	flog1.write(prnDict(P))
	Path = []
	#TODO: 加入exception
	reach=0
	if P.has_key(end):
		reach=1
    #P的引用有问题！
#	elif end not in P.keys():
#		for i_key in P.keys():
#			if end==P[i_key]:
#				reach=1
#				break	
	else:
		reach=0
	if reach==1:
	   while 1:
		   Path.append(end)
		   if end == start: break
		   end = P[end]
	   Path.reverse()
	   return Path
	else:
	   return Path



#G = {'s':{'u':9, 'x':5},'v':{'y':4},'x':{'y':4,'s':3},'u':{'y':1,'z':3}}
#D1,P1=Dijkstra(G,'s','v')
#print D1
#print P1
#print shortestPath(G,'s','v')



#As an example of the input format, here is the graph from Cormen, Leiserson, 
#	and Rivest (Introduction to Algorithms, 1st edition), page 528:
#G = {'s':{'u':10, 'x':5}, 'u':{'v':1, 'x':2}, 'v':{'y':4}, 
#     'x':{'u':3, 'v':9, 'y':2}, 'y':{'s':7, 'v':6}}
#The shortest path from s to v is ['s', 'x', 'u', 'v'] and has length 9.

#G = {'s':{'u':10, 'x':5}, 'u':{'v':1, 'x':2}, 'v':{'y':4}, 'x':{'u':3, 'v':9, 'y':2}, 'y':{'s':7, 'v':6}}
#Path = shortestPath(G,'s','v')
#print 'The shortest path from s to v: ', Path

# not reachable 
#G = {'s':{'u':10, 'x':5}, 'u':{'v':1, 'x':2}, 'v':{'y':4}, 'x':{'u':3, 'v':9, 'y':2}, 'y':{'v':6}}
#Path = shortestPath(G,'y','s')
#print 'The shortest path from y to s: ', Path

# test for 断头路
#G = {'s':{'u':10, 'x':5, 'p':7}, 'u':{'v':1, 'x':2}, 'v':{'y':4}, 'x':{'u':3, 'v':9, 'y':2}, 'y':{'v':6}}
#Path = shortestPath(G,'s','v')
#print 'The shortest path from s to v: ', Path
