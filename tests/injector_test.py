from pydi.annotation import dependency
from pydi.injector import partial_injector


def _f(n):
    return n * 2


def _g(n, m, f: dependency("f")):
    return f(n) + m


def test_partial_injector_dependencies():
    assert partial_injector.dependencies(_f) == set()
    assert partial_injector.dependencies(_g) == {"f"}


def test_partial_injector_inject():
    injected = partial_injector.inject(_g, {"f": _f})
    assert injected(5, 6) == 16
