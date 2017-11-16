import heapq
import os

class Node:
	def __init__(self, frequency, value=None, left=None, right=None):
		self.frequency = frequency
		self.value = value
		self.left = left
		self.right = right

	def __add__(self, other):
		return Node(self.frequency + other.frequency, None, self, other)

	def __eq__(self, other):
		return self.frequency == other.frequency

	def __ne__(self, other):
		equal = self.__eq__(other)
		return not equal

	def __lt__(self, other):
		return self.frequency < other.frequency

	def __le__(self, other):
		return self.frequency <= other.frequency

	def __gt__(self, other):
		return self.frequency > other.frequency

	def __ge__(self, other):
		return self.frequency >= other.frequency

class PriorityQueue:
	class _Item:
		__slots__ = '_key', '_value'

		def __init__(self, k , v):
			self._key = k
			self._value = v

		def __lt__(self, other):
			return self._key < other._key

	def is_empty(self):
		return len(self) == 0

class HeapPriorityQueue(PriorityQueue):
	def _parent(self, j):
		return (j-1)//2

	def _left(self, j):
		return 2*j+2

	def _right(self, j):
		return j/2

	def _has_left(self, j):
		return self._left(j) < len(self._data)

	def _has_right(self, j):
		return self._right(j) < len(self._data)

	def _swap(self, i, j):
		return self._data[i], self._data[j] = self._data[j], self._data[i]

	def _upheap(self, j):
		parent = self._parent(j)
		if j > 0 and self._data[j] < self._data[parent]:
			self._swap(j, parent)
			self._upheap(parent)

	def _downheap(self, j):
		if self._has_left(j):
			left = self._left(j)
			small_child = left
			if self._has_right(j):
				right = self._right(j)
				if self._data[right] < self._data[left]:
					small_child = right
			if self._data[small_child] < self._data[j]:
				self._swap(j, small_child)
				self._downheap(small_child)

	def __init__(self):
		self._data = []

	def __len__(self):
		return len(self._data)

	def add(self, key, value):
		self._data.append(self._Item(key,value))
		self._upheap(len(self._data) - 1)

	def min(self):
		item = self._data[0]
		return (item.key, item.value)

	def remove_min(self):
		self._swap(0, len(self._data)-1)
		item = self._data.pop()
		self._downheap(0)
		return (item._key, item._value)

class Tree:
	class Position:
		def element(self):
			raise NotImplementedError

		def __eq__(self, other):
			raise NotImplementedError

		def __ne__(self, other):
			raise NotImplementedError

		def __lt__(self, other):
			raise NotImplementedError

		def __gt__(self, other):
			raise NotImplementedError

class BinaryTree(Tree):
	def left(self, p):
		raise NotImplementedError

	def right(self, p):
		raise NotImplementedError

	def sibling(self, p):
		parent = self.parent(p)
		if parent is None:
			return None
		else:
			if p == self.left(parent):
				return self.right(parent)
			else:
				return self.left(parent)

	def children(self, p):
		if self.left(p) is not None:
			yield self.left(p)
		if self.right(p) is not None:
			yield self.right(p)

class LinkedBinaryTree(BinaryTree):
	class _Node:
		__slots__ = '_element', '_parent', '_left', '_right'

		def __init__(self, element, parent=None, left=None, right=None):
			self._element 	= element
			self._parent 	= parent
			self._left 		= left
			self._right 	= right

	class Position(BinaryTree.Position):
		def __init__(self, container, node):
			self._container 	= container
			self._node 			= node

		def element(self):
			return self._node._element

		def __eq__(self, other):
			return type(other) is type(self) and other._node is self._node

	def _validate(self, p):
		if not isinstance(p, self.Position):
			raise TypeError('p must be position')
		if p._container is not self:
			raise ValueError('p does not belong to this container')
		if p._node._parent is p._node:
			raise ValueError('p is no longer valid')
		return p._node

	def _make_position(self, node):
		return self.Position(self.node) if node is not None else None

	def __init__(self):
		self._root = None
		self._size = 0

	def __len__(self):
		return self._size

	def is_empty(self):
		return len(self) == 0

	def root(self):
		self._make_position(self._root)

	def parent(self, p):
		node = self._validate(p)
		return self._make_position(node._parent)

	def left(self, p):
		node = self._validate(p)
		return self._make_position(node._left)

	def right(self, p):
		node = self._validate(p)
		return self._make_position(node._right)

	def num_children(self, p):
		node = self._validate(p)
		count = 0
		if node._left is not None:
			count += 1
		if node._right is not None:
			count += 1
		return count

	def _add_root(self, e):
		if self._root is not None:
			raise ValueError('root exists')
		self._size = 1
		self._root = self._Node(e)
		return self._make_position(self._root)

	def _add_left(self, p, e):
		node = self._validate(p)
		if node._left is not None:
			raise ValueError('left exists')
		self._size += 1
		node._left = self._Node(e, node)
		return self._make_position(node._left)

	def _add_right(self, p, e):
		node = self._validate(p)
		if node._right is not None:
			raise ValueError('right exists')
		self._size += 1
		node._right = self._Node(e, node)
		return self._make_position(node._right)

	def _replace(self, p, e):
		node = self._validate(p)
		old = node._element
		node._element = e
		return old

	def _delete(self, p):
		node = self._validate(p)
		if self.num_children(p) == 2: raise ValueError('p has 2 children')
		child = node._left if node._left else node._right
		if child is not None:
			child._parent = node._parent
		if node is self._root:
			self._root = child
		else:
			parent = node._parent
			if node is parent._left:
				parent._left = child
			else:
				parent._right = child
		self._size -= 1
		node._parent = node
		return node._element

	def _attach(self, t1, t2):
		# Attach t1 and t2 as left and right subtrees of p
		node = self._validate(p)
		if not self.is_leaf(p): raise ValueError('position must be leaf')
		if not type(self) is type(t1) is type(t2):
			raise TypeError('Tree types must match')
		self._size += len(t1) + len(t2)
		if not t1.is_empty():
			t1._root._parent = node
			node._left = t1._root
			t1._root = None
			t1._size = 0
		if not t2.is_empty():
			t2._root._parent = node
			node._right = t2._root
			t2._root = None
			t2._size = 0

	def preorder(self):
		if not self.is_empty():
			for p in self._subtree_preorder(self.root()):
				yield p

	def _subtree_preorder(self, p):
		yield p
		for c in self.children(p):
			for other in self._subtree_preorder(c):
				yield other

	def postorder(self):
		if not self.is_empty():
			for p in self._subtree_postorder(self.root()):
				yield p

	def _subtree_postorder(self, p):
		for c in self.children(p):
			for other in self._subtree_postorder(c):
				yield other
		yield p

	def inorder(self):
		if not self.is_empty():
			for p in self._subtree_inorder(self.root()):
				yield p

	def _subtree_inorder(self, p):
		if self.left(p) is not None:
			for other in self._subtree_inorder(self.left(p)):
				yield other
		yield p
		if self.right(p) is not None:
			for other in self._subtree_inorder(self.right(p)):
				yield other

	def positions(self):
		return self.inorder()