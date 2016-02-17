from abc import ABCMeta, abstractmethod
import functools
import inspect

from styng.annotation import dependency


def _parameter_and_dependency_names(component):
    """Return the parameter names and respective dependency of the component."""
    signature = inspect.signature(component)
    return {parameter.name: parameter.annotation.name
            for parameter in signature.parameters.values()
            if isinstance(parameter.annotation, dependency)}


def _dependency_kwargs(component, dependencies):
    """Return the kwargs to be passed to the component to inject dependencies."""
    return {parameter_name: dependencies[dependency_name]
            for parameter_name, dependency_name
            in _parameter_and_dependency_names(component).items()}


class Injector(metaclass=ABCMeta):
    @abstractmethod
    def dependencies(self, component):
        """Return a set of dependencies for the given component."""

    @abstractmethod
    def inject(self, component, dependencies):
        """Inject the dependencies into the component."""


class PartialInjector(Injector):
    """Injector which partially applies callables to their dependencies."""

    def dependencies(self, component):
        parameter_and_dependency_names = _parameter_and_dependency_names(component)
        return set(parameter_and_dependency_names.values())

    def inject(self, component, dependencies):
        kwargs = _dependency_kwargs(component, dependencies)
        return functools.partial(component, **kwargs)


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
        kwargs = _dependency_kwargs(component, dependencies)
        return component(**kwargs)


class IdentityInjector(Injector):
    """Injector which returns components as-is."""

    def dependencies(self, component):
        return set()

    def inject(self, component, dependencies):
        return component


partial_injector = PartialInjector()
factory_injector = FactoryInjector()
identity_injector = IdentityInjector()
