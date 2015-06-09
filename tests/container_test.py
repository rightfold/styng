from pydi.annotation import dependency
from pydi.container import Container
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


def test_container():
    container = Container()
    container.install("f", _f, partial_injector)
    container.install("g", _g, partial_injector)
    container.install("c", _C, factory_injector)
    container.install("d", _D, factory_injector)
    assert container.resolve("g")(5, 6) == 16
    assert container.resolve("d").m(5, 6) == 16
