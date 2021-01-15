from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Collection, Optional, Iterable, Iterator, Reversible


class BaseLinkedNode(ABC, Collection):
    value: object

    def __repr__(self) -> str:
        self.next: Optional[BaseLinkedNode]
        return f'{self.__class__.__name__}(value={repr(self.value)}, ' \
               f'next={repr(self.next.value) if self.next is not None else "END"})'

    @classmethod
    @abstractmethod
    def from_iterable(cls, values: Iterable) -> Optional[BaseLinkedNode]:
        pass

    @abstractmethod
    def appendleft(self, value) -> BaseLinkedNode:
        pass

    @abstractmethod
    def popleft(self) -> tuple[BaseLinkedNode, object]:
        pass

    @abstractmethod
    def reverse(self):
        pass


class BaseDoublyLinkedNode(BaseLinkedNode, ABC, Reversible):
    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def append(self, value):
        pass


class BaseLinearLinkedNode(BaseLinkedNode, ABC):
    def __init__(self, value, next_: Optional[BaseLinearLinkedNode] = None):
        self.value = value
        self.next = next_

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


class BaseCircularLinkedNode(BaseLinkedNode, ABC):
    def __init__(self, value, next_: Optional[BaseCircularLinkedNode] = None):
        self.value = value
        self.next = next_ if next_ is not None else self

    def __len__(self, tail: Optional[BaseCircularLinkedNode] = None) -> int:
        if self is tail:
            return 0
        return 1 + self.next.__len__(self if tail is None else tail)

    def __iter__(self, tail: Optional[BaseCircularLinkedNode] = None) -> Iterator:
        if self is tail:
            return
        yield self.next.value
        yield from self.next.__iter__(self if tail is None else tail)

    def __contains__(self, value, tail: Optional[BaseCircularLinkedNode] = None) -> bool:
        if self is tail:
            return False
        return value == self.value or self.next.__contains__(value, self if tail is None else tail)