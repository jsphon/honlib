"""
Linked List for holding values.

For use in tracking changes to values.
"""

_inf = float("inf")


class Node:
    def __init__(self, t, v):
        self.t = t
        self.v = v
        self.next = None

    def __repr__(self):
        return f"<Node t={self.t}, v={self.v}>"


class ValueTracker:
    def __init__(self):
        sentinel = Node(t=float("-inf"), v=None)
        self.first = sentinel
        self.last = sentinel

    def __bool__(self):
        return self.first != self.last

    def append(self, t, v):
        if v != self.last.v:
            new_node = Node(t, v)
            self.last.next = new_node
            self.last = new_node

    def clear(self):
        sentinel = Node(t=float("-inf"), v=None)
        self.first = sentinel
        self.last = sentinel

    def to_tuple(self):
        return tuple((n.t, n.v) for n in self)

    def __iter__(self):
        node = self.first
        while node.next:
            yield node.next
            node = node.next

    def get_last_value(self):
        return self.last.v

    def tick(self, t):
        # Need to think of how we don't need this here
        pass


class NumberValueTracker(ValueTracker):
    def to_tuple_of_diffs(self):
        node = self.first
        prior_v = 0
        result = []
        while node.next:
            node = node.next
            result.append((node.t, node.v - prior_v))
            prior_v = node.v
        return tuple(result)


class TradedVolumeTracker(ValueTracker):
    def __init__(self, max_age=None):
        super(TradedVolumeTracker, self).__init__()
        self.max_age = max_age

    def append(self, t, v):
        """

        :param t:
        :param v:
            list of lists, price then size
        :return:
        """
        if v["diff"]:
            new_node = Node(t, v["diff"])
            self.last.next = new_node
            self.last = new_node
        self.tick(t)

    def tick(self, t):
        """
        Delete old nodes.
        :param t:
        :return:
        """

        if self.max_age:
            while (
                self.first.next
                and (t - self.first.t > self.max_age)
                and (t - self.first.next.t > self.max_age)
            ):
                self.first = self.first.next

    def max(self):
        mx = -_inf

        for node in self:
            mx = max(mx, max(node.v))

        return mx

    def min(self):
        if self:
            mn = min(min(node.v) for node in self if node.v)
        else:
            mn = _inf

        return mn


class WindowedValueTracker(ValueTracker):
    def __init__(self, max_age):
        super().__init__()
        self.max_age = max_age
        self.t = -float("inf")

    def append(self, t, v):
        super(WindowedValueTracker, self).append(t, v)
        self.tick(t)

    def tick(self, t):
        self.t = t
        while (
            self.first.next
            and (t - self.first.t > self.max_age)
            and (t - self.first.next.t > self.max_age)
        ):
            self.first = self.first.next

    def max(self):
        mx = -_inf
        for node in self:
            mx = max(mx, node.v)

        return mx

    def min(self):
        mn = _inf
        for node in self:
            mn = min(mn, node.v)

        return mn

    def median(self):
        summations = {}

        last_time = self.last.t

        current_node = self.first
        t0 = max(self.first.t, last_time - self.max_age)
        v0 = self.first.v

        while True:
            new_node = current_node.next
            if new_node:
                time_spent = new_node.t - t0
                if time_spent and v0:
                    summations[v0] = summations.get(v0, 0) + time_spent

                current_node = new_node
                t0 = new_node.t
                v0 = new_node.v
            else:
                time_spent = self.t - t0
                if time_spent and v0:
                    summations[v0] = summations.get(v0, 0) + time_spent
                break

        sorted_prices = sorted(summations)
        c = 0
        split = self.max_age / 2
        for i, price in enumerate(sorted_prices):
            c += summations[price]
            if c > split:
                return price
            elif c == split:
                if i < len(sorted_prices) - 1:
                    return 0.5 * (price + sorted_prices[i + 1])
