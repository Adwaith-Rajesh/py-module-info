import os

import pytest

from py_module_info import ModuleInfo


@pytest.fixture()
def code_to_test():
    code = """

def foo():
    pprint({"Hello": "World"})

    with open("test.json") as f:
        print(json.load(f))


def print_file_contents(z, x=None, y="str") -> None:
    with open(filename) as f:
        print(modify(load(f)))
        print(modify(json.load.test.some(f)))
        print(modify(json.load(f)))

    """

    with open("test_test.py", "w") as f:
        f.write(code)

    yield "test_test.py"
    os.remove("test_test.py")


def test_get_funcs_info(code_to_test):

    m = ModuleInfo(code_to_test)
    assert m.get_funcs_info() == {'foo': {'args': [], 'defaults': [], 'arg_count': 0, 'calls': ['json.load(f)', 'open("test.json")', 'pprint({"Hello": "World"})', 'print(json.load(f))']}, 'print_file_contents': {'args': ['z', 'x', 'y'], 'defaults': [None, 'str'], 'arg_count': 3, 'calls': [
        'json.load(f)', 'json.load.test.some(f)', 'load(f)', 'modify(json.load(f))', 'modify(json.load.test.some(f))', 'modify(load(f))', 'open(filename)', 'print(modify(json.load(f)))', 'print(modify(json.load.test.some(f)))', 'print(modify(load(f)))']}}


def test_get_funcs_info_with_only_funcs_names(code_to_test):
    m = ModuleInfo(code_to_test)
    assert m.get_funcs_info(only_func_names=True) == {'foo': {'args': [], 'defaults': [], 'arg_count': 0, 'calls': ['load', 'open', 'pprint', 'print']}, 'print_file_contents': {'args': ['z', 'x', 'y'], 'defaults': [None, 'str'], 'arg_count': 3, 'calls':
                                                                                                                                                                                 ['load', 'modify', 'open', 'print', 'some']}}
