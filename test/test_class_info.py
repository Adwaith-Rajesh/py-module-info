import os
from py_module_info import ModuleInfo

import pytest


@pytest.fixture()
def code_to_test():
    code = """

class Foo(A.Test):

    def __init__(self, name):
        self.name = name

    def n():
        pass

class Bar():

    def a():
        print('Hello')

    """

    with open("test_test.py", "w") as f:
        f.write(code)

    yield "test_test.py"
    os.remove("test_test.py")


def test_get_classes_info(code_to_test):

    m = ModuleInfo(code_to_test)
    assert m.get_classes_info() == {'Foo': {'bases': ['A.Test'], 'methods': {'__init__': {'args': ['self', 'name'], 'defaults': [], 'arg_count': 2, 'calls': []}, 'n': {'args': [], 'defaults': [], 'arg_count': 0,
                                                                                                                                                                        'calls': []}}}, 'Bar': {'bases': [], 'methods': {'a': {'args': [], 'defaults': [], 'arg_count': 0, 'calls': ["print('Hello')"]}}}}
