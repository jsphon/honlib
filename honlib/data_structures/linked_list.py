class Node:
    def __init__(self, v):
        self.v = v
        self.next = None

    def __repr__(self):
        return f"<Node t={self.t}, v={self.v}>"


class LinkedList:

    node_class = Node

    def __init__(self):
        sentinel = self.node_class(v=None)
        self.first = sentinel
        self.last = sentinel

    def __bool__(self):
        return self.first != self.last

    def append(self, v):
        if v != self.last.v:
            new_node = Node(v)
            self.last.next = new_node
            self.last = new_node

    def clear(self):
        sentinel = Node(v=None)
        self.first = sentinel
        self.last = sentinel

    def to_tuple(self):
        return tuple((n.v) for n in self)

    def __iter__(self):
        node = self.first
        while node.next:
            yield node.next
            node = node.next

    def get_last_value(self):
        return self.last.v


class DoublyLinkedListNode:
    def __init__(self, v):
        self.v = v
        self.next = None
        self.prev = None

    def __repr__(self):
        return f"<DoubledLinkedListNode value={self.v}>"


class DoublyLinkedList(LinkedList):

    node_class = DoublyLinkedListNode

    def append(self, v):
        if v != self.last.v:
            new_node = self.node_class(v)
            new_node.prev = self.last
            self.last.next = new_node
            self.last = new_node

    def __reversed__(self):
        node = self.last

        while node.prev:
            yield node
            node = node.prev