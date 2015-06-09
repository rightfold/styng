from pydi.annotation import dependency
from pydi.injector import factory_injector, partial_injector


def _f(n):
    return n * 2


def _g(n, m, f: dependency("f")):
    return f(n) + m


class _C:
    def m(self, n):
        return n * 2


class _D:
    def __init__(self, c: dependency("c")):
        self.__c = c

    def m(self, n, m):
        return self.__c.m(n) + m


def test_partial_injector_dependencies():
    assert partial_injector.dependencies(_f) == set()
    assert partial_injector.dependencies(_g) == {"f"}


def test_partial_injector_inject():
    injected = partial_injector.inject(_g, {"f": _f})
    assert injected(5, 6) == 16


def test_factory_injector_dependencies():
    assert factory_injector.dependencies(_C) == set()
    assert factory_injector.dependencies(_D) == {"c"}


def test_factory_injector_inject():
    injected = factory_injector.inject(_D, {"c": _C()})
    assert injected.m(5, 6) == 16
