from abc import ABCMeta, abstractmethod
import functools

from pydi.annotation import dependency


class Injector(metaclass=ABCMeta):
    @abstractmethod
    def dependencies(self, component):
        """Return a set of dependencies for the given component."""

    @abstractmethod
    def inject(self, component, dependencies):
        """Inject the dependencies into the component."""


class PartialInjector(Injector):
    """Injector which uses functools.partial to inject dependencies."""

    def dependencies(self, component):
        return {annotation.name
                for annotation in component.__annotations__.values()
                if isinstance(annotation, dependency)}

    def inject(self, component, dependencies):
        return functools.partial(component, **dependencies)


class ConstructorInjector(Injector):
    """Injector which instantiates classes by passing dependencies as constructor arguments."""

    def dependencies(self, component):
        raise NotImplemented()

    def inject(self, component, dependencies):
        raise NotImplemented()


partial_injector = PartialInjector()
constructor_injector = ConstructorInjector()
