class ComponentAlreadyInstalledError(Exception):
    pass


class ComponentNotInstalledError(KeyError):
    pass


class Container:
    """Register for components."""

    class __Installation:
        def __init__(self, component, injector):
            self.component = component
            self.injector = injector
            self.instantiated = False
            self.instantiation = None

    def __init__(self):
        """Initialize a new empty container."""
        self.__installations = {}

    def install(self, name, component, injector):
        """Install a component.

        A component with the same name must not already be installed.
        """
        if name in self.__installations:
            raise ComponentAlreadyInstalledError(name)
        self.__installations[name] = Container.__Installation(component, injector)

    def resolve(self, name):
        """Resolve a component and instantiate it if necessary.

        The component must already be installed.
        """
        if name not in self.__installations:
            raise ComponentNotInstalledError(name)
        installation = self.__installations[name]
        if not installation.instantiated:
            dependency_names = installation.injector.dependencies(installation.component)
            dependencies = {dependency: self.resolve(dependency)
                            for dependency in dependency_names}
            installation.instantiation = \
                installation.injector.inject(installation.component, dependencies)
            installation.instantiated = True
        return installation.instantiation
