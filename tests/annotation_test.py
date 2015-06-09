from styng.annotation import dependency


def test_dependency_name():
    name = 'dependency'
    annotation = dependency(name)
    assert annotation.name == name
