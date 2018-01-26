import os
from modules import Node
from collections import Counter
from itertools import groupby
from heapq import *

codes = {}

def read_file(f):
	binary = []
	with open(f, "rb") as s:
		byte = f.read(1)
		while byte != "":
			binary.append(byte)
	return binary

def count(binary):
	itemqueue = [Node(a, len(list(b))) for a, b in groupby(sorted(binary))]
	heapify(itemqueue)
	while len(itemqueue) > 1:
		l = heappop(itemqueue)
		r = heappop(itemqueue)
		n = Node(None, r.weight+l.weight)
		n.set_child(l, r)
		heappush(itemqueue, n)

def set_codes(s, node):
	if node.item:
		if not s:
			codes[node.item] = "0"
		else:
			codes[node.item] = s
	else:
		set_codes(s+"0", node.left)
		set_codes(s+"1", node.right)
	return codes










