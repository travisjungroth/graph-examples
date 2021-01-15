from __future__ import annotations
from typing import Optional, Iterable, Iterator

from graph_examples.linked_lists.base_nodes import BaseLinearLinkedNode, BaseDoublyLinkedNode, BaseCircularLinkedNode


class LinkedNode(BaseLinearLinkedNode):
    next: Optional[LinkedNode]

    @classmethod
    def from_iterable(cls, values: Iterable) -> Optional[LinkedNode]:
        values_iter = iter(values)
        try:
            node = cls(next(values_iter))
        except StopIteration:
            return None
        node.next = cls.from_iterable(values_iter)
        return node

    def appendleft(self, value) -> LinkedNode:
        return LinkedNode(value, self)

    def popleft(self) -> tuple[LinkedNode, object]:
        return self.next, self.value

    def reverse(self, last_node: Optional[LinkedNode] = None) -> LinkedNode:
        next_node = self.next
        self.next = last_node
        if next_node is None:
            return self
        return next_node.reverse(self)


class DoublyLinkedNode(BaseDoublyLinkedNode, BaseLinearLinkedNode):
    next: Optional[DoublyLinkedNode]
    last: Optional[DoublyLinkedNode]

    @classmethod
    def from_iterable(cls, values: Iterable, last: Optional[DoublyLinkedNode] = None) -> Optional[DoublyLinkedNode]:
        values_iter = iter(values)
        try:
            node = cls(next(values_iter), None, last)
        except StopIteration:
            return None
        node.next = cls.from_iterable(values_iter, node)
        return node

    @property
    def tail(self) -> DoublyLinkedNode:
        node = self
        while node.next is not None:
            node = node.next
        return node

    def __reversed__(self) -> Iterator:
        yield self.value
        if self.last is not None:
            yield from reversed(self.last)

    def append(self, value) -> DoublyLinkedNode:
        self.next = DoublyLinkedNode(value, None, self)
        return self.next

    def appendleft(self, value) -> DoublyLinkedNode:
        self.last = DoublyLinkedNode(value, self)
        return self.last

    def pop(self) -> tuple[DoublyLinkedNode, object]:
        if self.last is not None:
            self.last.next = None
        return self.last, self.value

    def popleft(self) -> tuple[DoublyLinkedNode, object]:
        if self.next is not None:
            self.next.last = None
        return self.next, self.value

    def reverse(self) -> DoublyLinkedNode:
        self.next, self.last = self.last, self.next
        if self.last is None:
            return self
        return self.last.reverse()


class CircularLinkedNode(BaseCircularLinkedNode):
    next: CircularLinkedNode

    @classmethod
    def from_iterable(cls, values: Iterable, head=None, last_node=None) -> Optional[CircularLinkedNode]:
        values_iter = iter(values)
        try:
            node = cls(next(values_iter), head)
            if last_node is not None:
                last_node.next = node
            return cls.from_iterable(values_iter, node if head is None else head, node)
        except StopIteration:
            return last_node

    def appendleft(self, value) -> CircularLinkedNode:
        self.next = CircularLinkedNode(value, self.next)
        return self

    def popleft(self) -> tuple[CircularLinkedNode, object]:
        value = self.next.value
        if self is self.next:
            return None, value
        else:
            self.next = self.next.next
            return self, value

    def reverse(self, last_node: Optional[CircularLinkedNode] = None,
                tail: Optional[CircularLinkedNode] = None) -> CircularLinkedNode:
        next_node = self.next
        self.next = last_node
        if next_node is None:
            return tail
        return next_node.reverse(self, next_node if tail is None else tail)


class CircularDoublyLinkedNode(BaseDoublyLinkedNode, BaseCircularLinkedNode):
    next: CircularDoublyLinkedNode
    last: CircularDoublyLinkedNode

    def __init__(
            self,
            value,
            next_: Optional[CircularDoublyLinkedNode] = None,
            last: Optional[CircularDoublyLinkedNode] = None
    ):
        next_ = next_ if next is not None else self
        last = last if last is not None else self
        super().__init__(value, next_, last)

    @classmethod
    def from_iterable(cls, values: Iterable, head=None, last_node=None) -> Optional[CircularDoublyLinkedNode]:
        values_iter = iter(values)
        try:
            node = cls(next(values_iter), head, last_node)
            if last_node is not None:
                last_node.next = node
                head.last = node
            return cls.from_iterable(values_iter, node if head is None else head, node)
        except StopIteration:
            return last_node

    def __reversed__(self, tail: Optional[CircularDoublyLinkedNode] = None) -> Iterator:
        if self is tail:
            return
        yield self.value
        yield from self.last.__reversed__(self if tail is None else tail)

    def append(self, value) -> CircularDoublyLinkedNode:
        self.next = CircularDoublyLinkedNode(value, self.next, self)
        self.next.next.last = self.next
        return self.next

    def appendleft(self, value) -> CircularDoublyLinkedNode:
        self.next = CircularDoublyLinkedNode(value, self.next, self)
        self.next.next.last = self.next
        return self

    def pop(self) -> tuple[CircularDoublyLinkedNode, object]:
        value = self.value
        if self is self.next:
            return None, value
        else:
            self.last.next = self.next
            self.next.last = self.last
            return self.last, value

    def popleft(self) -> tuple[CircularDoublyLinkedNode, object]:
        value = self.next.value
        if self is self.next:
            return None, value
        else:
            self.next = self.next.next
            self.next.last = self
            return self, value

    def reverse(self, head: Optional[CircularDoublyLinkedNode] = None) -> CircularDoublyLinkedNode:
        if self is head:
            return self.last
        self.next, self.last = self.last, self.next
        return self.last.reverse(self if head is None else head)
