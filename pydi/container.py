class ComponentAlreadyInstalledError(Exception):
    pass


class ComponentNotInstalledError(KeyError):
    pass


class Container:
    class __Installation:
        def __init__(self, component, injector):
            self.component = component
            self.injector = injector
            self.instantiated = False
            self.instantiation = None

    def __init__(self):
        self.__installations = {}

    def install(self, name, component, injector):
        if name in self.__installations:
            raise ComponentAlreadyInstalledError(name)
        self.__installations[name] = Container.__Installation(component, injector)

    def resolve(self, name):
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
