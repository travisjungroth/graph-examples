from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Collection, Iterable, Reversible, Iterator
from typing import Optional

from graph_examples.linked_lists.base_nodes import BaseLinearLinkedNode, BaseCircularLinkedNode, T


class BaseLinkedList(ABC, Collection[T]):
    # noinspection PyUnusedLocal
    @abstractmethod
    def __init__(self, values: Iterable[T] = ()) -> None:
        pass

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({repr([x for x in self])})'

    @abstractmethod
    def appendleft(self, value: T) -> None:
        pass

    @abstractmethod
    def popleft(self) -> T:
        pass

    @abstractmethod
    def reverse(self) -> None:
        pass


class BaseSinglyLinkedList(BaseLinkedList[T], ABC):
    pass


class BaseDoublyLinkedList(BaseLinkedList[T], ABC, Reversible):
    @abstractmethod
    def pop(self) -> T:
        pass

    @abstractmethod
    def append(self, value: T) -> None:
        pass


class BaseLinearLinkedList(BaseLinkedList, ABC):
    head: Optional[BaseLinearLinkedNode[T]]

    def __bool__(self) -> bool:
        return self.head is not None

    def __len__(self) -> int:
        length = 0
        node = self.head
        while node is not None:
            node = node.next
            length += 1
        return length

    def __iter__(self) -> Iterator[T]:
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def __contains__(self, value: T) -> bool:
        node = self.head
        while node is not None:
            if node.value == value:
                return True
            node = node.next
        return False


class BaseCircularLinkedList(BaseLinkedList[T], ABC):
    tail: Optional[BaseCircularLinkedNode[T]]
    head: Optional[BaseCircularLinkedNode[T]]

    def __bool__(self) -> bool:
        return self.tail is not None

    def __len__(self) -> int:
        if not self:
            return 0
        length = 1
        node = self.head
        while node is not self.tail:
            length += 1
            node = node.next
        return length

    def __iter__(self) -> Iterator[T]:
        if not self:
            return
        head = self.head
        yield head.value
        node = head.next
        while node is not head:
            yield node.value
            node = node.next

    def infinite_iterator(self):
        if not self:
            return
        node = self.head
        while True:
            yield node.value
            node = node.next

    def __contains__(self, value: T) -> bool:
        if not self:
            return False
        node = self.head
        while node is not self.tail:
            if node.value == value:
                return True
            node = node.next
        return self.tail.value == value

    def popleft(self) -> T:
        if not self:
            raise IndexError
        value = self.head.value
        if self.tail is self.head:
            self.tail = None
        else:
            self.head = self.head.next
        return value
