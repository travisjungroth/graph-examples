from abc import ABC
from typing import TypeVar

from pytest import mark, fixture, raises

from graph_examples import AbstractLinkedNode, AbstractLinkedList, AbstractDoublyLinkedList

T = TypeVar('T')


def concrete_subclasses(cls: T, *except_: T) -> list[T]:
    except_ = set(except_)
    seen = {cls}
    queue = [cls]
    concrete = []
    while queue:
        for cls in set(queue.pop(0).__subclasses__()) - seen - except_:
            seen.add(cls)
            queue.append(cls)
            if ABC not in cls.__bases__:
                concrete.append(cls)
    return concrete


@fixture(params=['a', 'ab', 'abc'])
def letters(request) -> str:
    return request.param


@fixture(params=['', 'a', 'ab', 'abc'])
def letters_and_empty(request) -> str:
    return request.param


@mark.parametrize('cls', concrete_subclasses(AbstractLinkedNode))
class TestAbstractLinkedNode:
    def test_len(self, cls, letters):
        node = cls.from_iterable(letters)
        assert len(node) == len(letters)

    def test_iter(self, cls, letters):
        node = cls.from_iterable(letters)
        assert list(node) == list(letters)

    def test_contains(self, cls, letters):
        node = cls.from_iterable(letters)
        for letter in letters:
            assert letter in node
        assert object() not in node

    def test_appendleft(self, cls, letters):
        node = cls.from_iterable(letters)
        node = node.appendleft('x')
        assert list(node) == list('x' + letters)

    def test_popleft(self, cls, letters):
        node = cls.from_iterable(letters)
        values = []
        while node:
            node, value = node.popleft()
            values.append(value)
        assert node is None
        assert values == list(letters)

    def test_reverse(self, cls, letters):
        node = cls.from_iterable(letters)
        node = node.reverse()
        assert list(node) == list(reversed(letters))


@mark.parametrize('cls', concrete_subclasses(AbstractLinkedList))
class TestAbstractLinkedList:
    def test_len(self, cls, letters_and_empty):
        li = cls(letters_and_empty)
        assert len(li) == len(letters_and_empty)

    def test_iter(self, cls, letters_and_empty):
        li = cls(letters_and_empty)
        assert list(li) == list(letters_and_empty)

    def test_contains(self, cls, letters_and_empty):
        li = cls(letters_and_empty)
        for letter in letters_and_empty:
            assert letter in li
        assert object() not in li

    def test_bool(self, cls, letters_and_empty):
        li = cls(letters_and_empty)
        assert bool(li) == bool(letters_and_empty)

    def test_appendleft(self, cls, letters_and_empty):
        li = cls(letters_and_empty)
        li.appendleft('x')
        assert list(li) == list('x' + letters_and_empty)

    def test_popleft(self, cls, letters_and_empty):
        li = cls(letters_and_empty)
        values = []
        while li:
            value = li.popleft()
            values.append(value)
        assert not li
        assert values == list(letters_and_empty)

    def test_popleft_empty(self, cls):
        li = cls()
        with raises(IndexError):
            li.popleft()

    def test_reverse(self, cls, letters_and_empty):
        li = cls(letters_and_empty)
        li.reverse()
        assert list(li) == list(reversed(letters_and_empty))


@mark.parametrize('cls', concrete_subclasses(AbstractDoublyLinkedList))
class TestAbstractDoublyLinkedList:
    def test_reversed(self, cls, letters_and_empty):
        li = cls(letters_and_empty)
        assert list(reversed(li)) == list(reversed(letters_and_empty))

    def test_pop(self, cls, letters_and_empty):
        li = cls(letters_and_empty)
        values = []
        while li:
            value = li.pop()
            values.append(value)
        assert not li
        assert values == list(reversed(letters_and_empty))

    def test_pop_empty(self, cls):
        li = cls()
        with raises(IndexError):
            li.pop()

    def test_append(self, cls, letters_and_empty):
        li = cls(letters_and_empty)
        li.append('x')
        assert list(li) == list(letters_and_empty + 'x')
