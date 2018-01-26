import heapq
import os

class Node(object):
	left = None
	right = None
	item = None
	weight = None

	def __init__(self, i, w):
		self.item = i
		self.weight = w

	def set_child(self, ln, rn):
		self.left = ln
		self.right = rn

	def __repr__(self):
		return '%s - %s - %s _ %s' % (self.item, self.weight,
			self.left, self.right)

	def __cmp__(self, a):
		return cmp(self.weight, a.weight)

