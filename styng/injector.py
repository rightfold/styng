from abc import ABCMeta, abstractmethod
import functools
import inspect

from styng.annotation import dependency


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
        signature = inspect.signature(component)
        return {parameter.annotation.name
                for parameter in signature.parameters.values()
                if isinstance(parameter.annotation, dependency)}

    def inject(self, component, dependencies):
        return functools.partial(component, **dependencies)


class FactoryInjector(Injector):
    """Injector which applies callables to their dependencies."""

    class NonDependencyParameter(ValueError):
        """The factory has a parameter without a dependency annotation."""

    def dependencies(self, component):
        signature = inspect.signature(component)
        dependencies = set()
        for parameter in signature.parameters.values():
            annotation = parameter.annotation
            if not isinstance(annotation, dependency):
                raise FactoryInjector.NonDependencyParameter(parameter.name)
            dependencies.add(annotation.name)
        return dependencies

    def inject(self, component, dependencies):
        return component(**dependencies)


class IdentityInjector(Injector):
    """Injector which returns components as-is."""

    def dependencies(self, component):
        return set()

    def inject(self, component, dependencies):
        return component


partial_injector = PartialInjector()
factory_injector = FactoryInjector()
identity_injector = IdentityInjector()