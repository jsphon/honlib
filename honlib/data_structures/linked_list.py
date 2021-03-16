class Node:
    def __init__(self, v):
        self.v = v
        self.next = None

    def __repr__(self):
        return f"<Node t={self.t}, v={self.v}>"


class LinkedList:
    def __init__(self):
        sentinel = Node(v=None)
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
