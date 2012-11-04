import main
import heapq
from collections import defaultdict
from Config import Config

path_back = defaultdict(lambda: None)

def dist(x, y):
	return (x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2

def pathable(p0, pf):
	return False

def children(p):
	x, y = p
	d = Config['PIXELS_PER_TILE']
	return [(x-d, y-d), (x-d, y), (x-d, y+d), (x, y-d), (x, y), (x, y+d), (x+d, y-d), (x+d, y), (x+d, y+d)]

def path_to(start, fin):
	front = [(dist(fin, start), fin[0], fin[1])]
	heapq.heapify(front)
	closed = set()
	
	while True:
		nxt = heapq.heappop(front)
		nxt = (nxt[1], nxt[2])
		closed.add(c)
		if nxt[0] == start[0] and nxt[1] == start[1]:
			return path_back[start]
		
		for c in children(nxt)
			if c in closed: continue
			if not pathable(nxt, c): continue
			path_back[c] = nxt
			heapq.heappush((dist(start, c) + dist(c, fin), c[0], c[1]))
