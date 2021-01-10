from abc import ABC
from typing import TypeVar

from pytest import mark, fixture

from graph_examples import AbstractLinkedNode

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
