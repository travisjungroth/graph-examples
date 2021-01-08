from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Collection, Iterable, Iterator, Optional


class AbstractLinkedNode(ABC, Collection):
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.from_iterable({repr([x for x in self])})'

    @classmethod
    @abstractmethod
    def from_iterable(cls, values: Iterable) -> Optional[AbstractLinkedNode]:
        pass

    @abstractmethod
    def appendleft(self, value) -> AbstractLinkedNode:
        pass

    @abstractmethod
    def popleft(self) -> tuple[AbstractLinkedNode, object]:
        pass

    @abstractmethod
    def reverse(self):
        pass


class LinkedNode(AbstractLinkedNode):
    def __init__(self, value, next_: Optional[LinkedNode] = None):
        self.value = value
        self.next = next_

    @classmethod
    def from_iterable(cls, values: Iterable) -> Optional[LinkedNode]:
        values_iter = iter(values)
        try:
            head = cls(next(values_iter))
        except StopIteration:
            return None
        node = head
        for value in values_iter:
            node.next = cls(value)
            node = node.next
        return head

    def __len__(self) -> int:
        if self.next is None:
            return 1
        return 1 + len(self.next)

    def __iter__(self) -> Iterator:
        yield self.value
        if self.next is not None:
            yield from self.next

    def __contains__(self, value) -> bool:
        if value == self.value:
            return True
        return self.next is not None and value in self.next

    def appendleft(self, value) -> LinkedNode:
        return LinkedNode(value, self)

    def popleft(self) -> tuple[LinkedNode, object]:
        head = self.next
        self.next = None
        return head, self.value

    def reverse(self, last_node: Optional[LinkedNode] = None):
        next_node = self.next
        self.next = last_node
        if next_node is None:
            return self
        return next_node.reverse(self)


class CircularLinkedNode(AbstractLinkedNode):
    def __init__(self, value, next_: Optional[CircularLinkedNode] = None):
        self.value = value
        self.next = next_

    @classmethod
    def from_iterable(cls, values: Iterable) -> Optional[CircularLinkedNode]:
        values_iter = iter(values)
        try:
            head = cls(next(values_iter))
        except StopIteration:
            return None
        node = head
        for value in values_iter:
            node.next = cls(value)
            node = node.next
        node.next = head
        return node

    def __len__(self, tail: Optional[CircularLinkedNode] = None) -> int:
        if self is tail:
            return 0
        return 1 + self.next.__len__(self if tail is None else tail)

    def __iter__(self, tail: Optional[CircularLinkedNode] = None) -> Iterator:
        if self is tail:
            return
        yield self.next.value
        yield from self.next.__iter__(self if tail is None else tail)

    def __contains__(self, value, tail: Optional[CircularLinkedNode] = None) -> bool:
        if self is tail:
            return False
        return value == self.value or self.next.__contains__(value, self if tail is None else tail)

    def appendleft(self, value) -> CircularLinkedNode:
        self.next = CircularLinkedNode(value, self.next)
        return self.next

    def popleft(self) -> tuple[CircularLinkedNode, object]:
        value = self.next.value
        self.next = self.next.next if self.next is not self else None
        return self.next, value

    def reverse(self):
        pass


class AbstractLinkedList(ABC, Collection):
    # noinspection PyUnusedLocal
    @abstractmethod
    def __init__(self, values: Iterable = ()):
        pass

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({repr([x for x in self])})'

    @abstractmethod
    def appendleft(self, value):
        pass

    @abstractmethod
    def popleft(self):
        pass

    @abstractmethod
    def reverse(self):
        pass


class LinkedList(AbstractLinkedList):
    def __init__(self, values: Iterable = ()):
        values_iter = iter(values)
        try:
            self.head = LinkedNode(next(values_iter))
        except StopIteration:
            self.head = None
        else:
            node = self.head
            for value in values_iter:
                node.next = LinkedNode(value)
                node = node.next

    def __len__(self) -> int:
        length = 0
        node = self.head
        while node is not None:
            node = node.next
            length += 1
        return length

    def __iter__(self) -> Iterator:
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def __contains__(self, value) -> bool:
        node = self.head
        while node is not None:
            if node.value == value:
                return True
            node = node.next
        return False

    def appendleft(self, value):
        self.head = LinkedNode(value, self.head)

    def popleft(self):
        node = self.head
        self.head = node.next
        return node.value

    def reverse(self):
        node = self.head
        last_node = None
        while node is not None:
            node.next, last_node, node = last_node, node, node.next
        self.head = last_node
