from functools import reduce, wraps
from typing import Callable, Any, List

E = Any
A = B = C = Any


class Option:
    __slots__ = ["_value"]

    def __init__(self, value: A):
        self._value = value

    def __iter__(self):
        return iter([self._value])

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self._value)})"

    @staticmethod
    def lift(f: Callable[[A], B]):
        def _(option):
            return option.map(f)

    def map(self, f: Callable[[A], B]):
        """Subclass need rewrite this method"""

    def flat_map(self, f):
        """Subclass need rewrite this method"""

    def map2(self, b):
        def _(f: Callable[[A, B], C]):
            return self.flat_map(lambda a: b.map(lambda b1: f(a, b1)))

        return _


class Some(Option):
    __slots__ = ["_value"]

    def __init__(self, value: A = None):
        super().__init__(value)

    def __repr__(self):
        if self._value is None:
            return "Null"
        else:
            return f"Some({repr(self._value)})"

    @property
    def isnil(self):
        return self._value is None

    def map(self, f: Callable[[A], B]) -> Option:
        if self.isnil:
            return Nil
        else:
            return self.__class__(f(self._value))

    def flat_map(self, f: Callable[[A], Option]) -> Option:
        if self.isnil:
            return Nil
        else:
            return f(self._value)

    def filter(self, f: Callable[[A], bool]) -> Option:
        if self.isnil or not f(self._value):
            return Nil
        else:
            return self

    @staticmethod
    def traverse(a: List[A]):
        """List[A] => Option[List[A]]"""
        def _(f: Callable[[A], Option]):
            return reduce(lambda t, h: t.map2(f(h))(lambda x, y: x + [y]), a, Some([]))

        return _

    @staticmethod
    def sequence(a: List[A]):
        """List[A] => Option[List[A]]"""
        return Some.traverse(a)(lambda x: x)

    def get_or_else(self, default: B) -> A:
        if self.isnil:
            return default
        else:
            return self._value

    def or_else(self, b: Option) -> Option:
        if self.isnil:
            return b
        else:
            return self

    def if_present(self, func: Callable[[A]]):
        if not self.isnil:
            func(self._value)


Nil = Some()


class Left(Option):
    __slots__ = ["_value"]

    def __init__(self, err: Exception):
        super().__init__(err)

    def map(self, f: Callable[[A], B]):
        return self

    def flat_map(self, f: Callable[[A], Option]):
        return self

    @staticmethod
    def or_else(b: Option):
        return b


class Right(Option):
    __slots__ = ["_value"]

    def __init__(self, value: A):
        super().__init__(value)

    def map(self, f: Callable[[A], B]):
        return Right(f(self._value))

    def flat_map(self, f: Callable[[A], Option]) -> Option:
        return f(self._value)

    def or_else(self, b: Option):
        return self


def try_except(func: Callable):

    # noinspection PyBroadException
    @wraps(func)
    def wrapped(*args, details=False, **kwargs):
        if details:
            try:
                return Right(func(*args, **kwargs))
            except Exception as e:
                return Left(e)
        else:
            try:
                return Some(func(*args, **kwargs))
            except Exception:
                return Nil
    return wrapped
