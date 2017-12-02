import os
from modules import Node, HeapPriorityQueue, LinkedBinaryTree
from collections import Counter

def read_file(f):
	binary = []
	with open(f, "rb") as s:
		byte = f.read(1)
		while byte != "":
			binary.append(byte)
	return binary

def count_freq(f):
	s = read_file(f)
	count = collections.Counter(s)
	return count

def build_tree(f):
	c = count_freq(f)
	tree = LinkedBinaryTree()
	tree._add_root(c[0])
	for j in c[1:]:
		left = tree.left(j)
	return tree

def traverse_tree(f):
	t = build_tree(f)
	root = t.root()
	if t.is_empty():
		return None
	else:
		children = t.children()
		return children







