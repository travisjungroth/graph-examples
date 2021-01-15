from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Collection, Optional, Iterable, Iterator, Reversible


class BaseLinkedNode(ABC, Collection):
    """The Abstract Base Class for all nodes in linked lists.

    BaseLinkedNodes will favor recursion over iteration in their methods.
    The default is for operations to be done from the head of the list,
    and for methods that return a node to return the head.

    Attributes:
        value: The value that occupies this position in the list.
        next: The next node in the list. None indicates no node.
    """

    def __init__(self, value: object, next_: Optional[BaseLinkedNode] = None):
        self.value = value
        self.next = next_

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(value={repr(self.value)}, ' \
               f'next={repr(self.next.value) if self.next is not None else "END"})'

    @classmethod
    @abstractmethod
    def from_iterable(cls, values: Iterable) -> Optional[BaseLinkedNode]:
        """Recursively create a new list of nodes.

        Args:
            values: Any iterable that will populate the new list, preserving order.

        Returns:
            The head of the new list.
        """

    @abstractmethod
    def appendleft(self, value: object) -> BaseLinkedNode:
        """Append to the left side of the list, which is also the 0th and head.

        Args:
            value: The value that goes on the new head.

        Returns:
            The new head of the list with the value set.
        """

    @abstractmethod
    def popleft(self) -> tuple[BaseLinkedNode, object]:
        """Pop from the left side of the list, which is also the 0th and head.

        Returns:
            A tuple of (node that is now the head, value from old head).
        """

    @abstractmethod
    def reverse(self) -> BaseLinkedNode:
        """Recursively reverse the list.

        Returns:
            The new head.
        """


class BaseSinglyLinkedNode(BaseLinkedNode, ABC):
    """A list with just a next node and no last.

    This class has no attributes or methods over the BaseLinkedNode, but exists for inheritance clarity."""


class BaseDoublyLinkedNode(BaseLinkedNode, ABC, Reversible):
    """The Abstract Base Class for all doubly linked nodes in linked lists.

    BaseDoublyLinkedNode introduces a "last" attribute. This allows methods on the right side of the list to be done
    in appropriate time complexity.

    Attributes:
        value: The value that occupies this position in the list.
        next: The next node in the list. None indicates no node.
        last: The last node in the list. None indicates no node.
    """

    def __init__(self,
                 value: object,
                 next_: Optional[BaseDoublyLinkedNode] = None,
                 last: Optional[BaseDoublyLinkedNode] = None):
        super().__init__(value, next_)
        self.last = last

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(value={repr(self.value)}, ' \
               f'next={repr(self.next.value) if self.next is not None else "END"}, ' \
               f'last={repr(self.last.value) if self.last is not None else "END"})'

    @abstractmethod
    def pop(self):
        """Pop from the right side of the list, which is also the 0th and head.

        Returns:
            A tuple of (node that is now the head, value from old head).
        """

    @abstractmethod
    def append(self, value):
        """Append to the ride side of the list, which is also the -1th and tail.

        Args:
            value: The value that goes on the new tail.

        Returns:
            The new tail of the list with the value set.
        """


class BaseLinearLinkedNode(BaseLinkedNode, ABC):
    """The Abstract Base Class for all linear (non-circular) linked nodes in linked lists.

    Any references to nodes should be optional, with None being considered terminal. Any introduced references to nodes
    should follow this pattern.
    """

    def __len__(self) -> int:
        """Recursively get the count of this node and the nodes that come after it."""
        if self.next is None:
            return 1
        return 1 + len(self.next)

    def __iter__(self) -> Iterator:
        """Recursively iterate through the nodes.

        Yields:
            The values from this node and the ones after it.
        """
        yield self.value
        if self.next is not None:
            yield from self.next

    def __contains__(self, value: object) -> bool:
        """Recursively search for the value on this node and the ones after in O(n) time."""
        if value == self.value:
            return True
        return self.next is not None and value in self.next


class BaseCircularLinkedNode(BaseLinkedNode, ABC):
    """The Abstract Base Class for all circular linked nodes in linked lists.

    Args:
        value: The value that occupies this position in the list.
        next: The next node in the list. This is no longer optional. If nothing is provided, defaults to self.
    """
    next: BaseCircularLinkedNode

    def __init__(self, value: object, next_: Optional[BaseCircularLinkedNode] = None):
        next_ = next_ if next_ is not None else self
        super().__init__(value, next_)

    def __len__(self, tail: Optional[BaseCircularLinkedNode] = None) -> int:
        """Recursively get the count of this node and the nodes that come after it."""
        if self is tail:
            return 0
        return 1 + self.next.__len__(self if tail is None else tail)

    def __iter__(self, tail: Optional[BaseCircularLinkedNode] = None) -> Iterator:
        """Recursively iterate through the nodes.

        Yields:
            The values from this node and the ones after it.
        """
        if self is tail:
            return
        yield self.next.value
        yield from self.next.__iter__(self if tail is None else tail)

    def __contains__(self, value, tail: Optional[BaseCircularLinkedNode] = None) -> bool:
        """Recursively search for the value on this node and the ones after in O(n) time."""
        if self is tail:
            return False
        return value == self.value or self.next.__contains__(value, self if tail is None else tail)
