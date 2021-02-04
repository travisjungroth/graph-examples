"""The concrete implementations of nodes for linked lists.

The naming convention for these classes is that singly and linear linked is the default and doesn't go in the class
name. While this is less precise, it matches the convention."""

from __future__ import annotations
from collections.abc import Iterable, Iterator
from typing import Optional, Type, TypeVar

from graph_examples.linked_lists.base_nodes import (
    BaseLinearLinkedNode,
    BaseDoublyLinkedNode,
    BaseCircularLinkedNode,
    BaseSinglyLinkedNode,
    T,
)


class LinkedNode(BaseSinglyLinkedNode[T], BaseLinearLinkedNode[T]):
    """The most basic node on a linked list."""
    next: Optional[LinkedNode[T]]

    @classmethod
    def from_iterable(cls: Type[LinkedNode], values: Iterable[T]) -> LinkedNode[T]:
        """Recursively create a new list of nodes.

        Args:
            values: Any iterable that will populate the new list, preserving order.

        Returns:
            The head of the new list.
        """
        values_iter = iter(values)
        try:
            node = cls(next(values_iter))
        except StopIteration:
            return None  # Ends the recursion and assigns None as next for the last node
        node.next = cls.from_iterable(values_iter)
        return node

    def appendleft(self, value) -> LinkedNode[T]:
        """Append to the left side of the list, which is also the 0th and head.

        Args:
            value: The value that goes on the new head.

        Returns:
            The new head of the list with the value set.
        """
        return LinkedNode(value, self)

    def popleft(self) -> tuple[LinkedNode[T], T]:
        """Pop from the left side of the list, which is also the 0th and head.

        Returns:
            A tuple of (node that is now the head, value from old head).
        """
        return self.next, self.value

    def reverse(self, last_node: Optional[LinkedNode[T]] = None) -> LinkedNode[T]:
        """Recursively reverse the list.

        Returns:
            The new head.
        """
        next_node = self.next
        self.next = last_node
        if next_node is None:
            return self  # We've hit the old tail, which is now the head.
        return next_node.reverse(self)


class DoublyLinkedNode(BaseDoublyLinkedNode[T], BaseLinearLinkedNode[T]):
    """A node on a doubly linear linked list.

    When working with this class, it is useful to hold onto both the head and tail nodes.
    Left side operations (appendleft, popleft, __iter__, reverse) are done from the head.
    Right side operations (append, pop, __reversed__) are done from the tail.
    """
    next: Optional[DoublyLinkedNode[T]]
    last: Optional[DoublyLinkedNode[T]]

    @classmethod
    def from_iterable(cls, values: Iterable[T], last: Optional[DoublyLinkedNode] = None) -> Optional[DoublyLinkedNode[T]]:
        """Recursively create a new list of nodes.

        Args:
            values: Any iterable that will populate the new list, preserving order.
            last: The previous node that was created. This is needed to assign last on the new nodes.

        Returns:
            The head of the new list.
        """
        values_iter = iter(values)
        try:
            node = cls(next(values_iter), None, last)
        except StopIteration:
            return None
        node.next = cls.from_iterable(values_iter, node)
        return node

    @property
    def tail(self) -> DoublyLinkedNode[T]:
        """Grab the tail from the current node. O(n). Useful for doing tail-side operations.

        Returns:
            The tail of the list of nodes
        """
        if self.next is None:
            return self
        return self.next.tail

    def __reversed__(self) -> Iterator[T]:
        """Yields:
            The values from this node to the head, backwards.
        """
        yield self.value
        if self.last is not None:
            yield from reversed(self.last)

    def append(self, value: T) -> DoublyLinkedNode[T]:
        """This should be called from the tail and appends to the ride side of the list.

        Args:
            value: The value that goes on the new tail.

        Returns:
            The new tail of the list with the value set.
        """
        self.next = DoublyLinkedNode(value, None, self)
        return self.next

    def appendleft(self, value: T) -> DoublyLinkedNode[T]:
        """This should be called from the head and appends to the left side of the list.

        Args:
            value: The value that goes on the new head.

        Returns:
            The new head of the list with the value set.
        """
        self.last = DoublyLinkedNode(value, self)
        return self.last

    def pop(self) -> tuple[DoublyLinkedNode[T], T]:
        """This should be called from the tail and pops from the right side of the list.

        Returns:
            A tuple of (node that is now the head, value from old head).
        """
        if self.last is not None:
            self.last.next = None
        return self.last, self.value

    def popleft(self) -> tuple[DoublyLinkedNode[T], T]:
        """This should be called from the head and pops from the left side of the list.

        Returns:
            A tuple of (node that is now the head, value from old head).
        """
        if self.next is not None:
            self.next.last = None
        return self.next, self.value

    def reverse(self) -> DoublyLinkedNode[T]:
        """Recursively reverse the list. Call from the head.

        Returns:
            The new head.
        """
        self.next, self.last = self.last, self.next
        if self.last is None:
            return self
        return self.last.reverse()


class CircularLinkedNode(BaseSinglyLinkedNode[T], BaseCircularLinkedNode[T]):
    next: CircularLinkedNode[T]

    @classmethod
    def from_iterable(cls, values: Iterable[T], head=None, last_node=None) -> Optional[CircularLinkedNode[T]]:
        values_iter = iter(values)
        try:
            node = cls(next(values_iter), head)
            if last_node is not None:
                last_node.next = node
            return cls.from_iterable(values_iter, node if head is None else head, node)
        except StopIteration:
            return last_node

    def appendleft(self, value: T) -> CircularLinkedNode[T]:
        self.next = CircularLinkedNode(value, self.next)
        return self

    def popleft(self) -> tuple[CircularLinkedNode[T], T]:
        value = self.next.value
        if self is self.next:
            return None, value
        else:
            self.next = self.next.next
            return self, value

    def reverse(self, last_node: Optional[CircularLinkedNode] = None,
                tail: Optional[CircularLinkedNode] = None) -> CircularLinkedNode[T]:
        next_node = self.next
        self.next = last_node
        if next_node is None:
            return tail
        return next_node.reverse(self, next_node if tail is None else tail)


class CircularDoublyLinkedNode(BaseDoublyLinkedNode[T], BaseCircularLinkedNode[T]):
    next: CircularDoublyLinkedNode[T]
    last: CircularDoublyLinkedNode[T]

    def __init__(
            self,
            value,
            next_: Optional[CircularDoublyLinkedNode] = None,
            last: Optional[CircularDoublyLinkedNode] = None
    ) -> None:
        next_ = next_ if next is not None else self
        last = last if last is not None else self
        super().__init__(value, next_, last)

    @classmethod
    def from_iterable(cls, values: Iterable[T], head=None, last_node=None) -> Optional[CircularDoublyLinkedNode[T]]:
        values_iter = iter(values)
        try:
            node = cls(next(values_iter), head, last_node)
            if last_node is not None:
                last_node.next = node
                head.last = node
            return cls.from_iterable(values_iter, node if head is None else head, node)
        except StopIteration:
            return last_node

    @property
    def tail(self):
        return self

    def __reversed__(self, tail: Optional[CircularDoublyLinkedNode] = None) -> Iterator:
        if self is tail:
            return
        yield self.value
        yield from self.last.__reversed__(self if tail is None else tail)

    def append(self, value: T) -> CircularDoublyLinkedNode[T]:
        self.next = CircularDoublyLinkedNode(value, self.next, self)
        self.next.next.last = self.next
        return self.next

    def appendleft(self, value: T) -> CircularDoublyLinkedNode[T]:
        self.next = CircularDoublyLinkedNode(value, self.next, self)
        self.next.next.last = self.next
        return self

    def pop(self) -> tuple[CircularDoublyLinkedNode[T], T]:
        value = self.value
        if self is self.next:
            return None, value
        else:
            self.last.next = self.next
            self.next.last = self.last
            return self.last, value

    def popleft(self) -> tuple[CircularDoublyLinkedNode[T], T]:
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
