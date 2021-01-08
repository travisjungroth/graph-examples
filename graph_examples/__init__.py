from abc import ABC, abstractmethod
from typing import Collection, Iterable, Iterator, Optional


class AbstractLinkedNode(ABC):
    pass


class LinkedNode(AbstractLinkedNode):
    def __init__(self, value, next_: Optional[AbstractLinkedNode] = None):
        self.value = value
        self.next = next_


class AbstractLinkedList(ABC, Collection):
    @abstractmethod
    def __init__(self, values: Iterable = ()):
        pass

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
        node: LinkedNode = self.head
        for value in values_iter:
            node.next = LinkedNode(value)
            node = node.next

    def __iter__(self) -> Iterator:
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def __len__(self) -> int:
        length = 0
        node = self.head
        while node is not None:
            node = node.next
            length += 1
        return length

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
