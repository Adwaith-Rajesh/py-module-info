import ast
import os

import pytest

from py_module_info import ModuleInfo


@pytest.fixture()
def code_to_test():
    code = """
import json
import pprint as p
from typing import List as l
from json import load, dump as d
from py_module_info.main import ModuleInfo
    """

    with open("test_test.py", "w") as f:
        f.write(code)

    yield "test_test.py"
    os.remove("test_test.py")


@pytest.fixture()
def split_test():
    code = """
import json, pprint, types, typing as t
    """
    with open("test_test.py", "w") as f:
        f.write(code)

    yield "test_test.py"
    os.remove("test_test.py")


def test_imported_names(code_to_test):

    m = ModuleInfo(code_to_test).get_imports()
    assert m.get_imported_names() == [
        'json', 'pprint', 'List', 'load', 'dump', 'ModuleInfo']
    assert m.get_imported_names(use_alias=True) == [
        'json', 'p', 'l', 'load', 'd', 'ModuleInfo']


def test_import_strings(code_to_test):
    m = ModuleInfo(code_to_test).get_imports()
    assert m.get_import_strings() == ['import json', 'import pprint', 'from typing import List',
                                      'from json import load', 'from json import dump', 'from py_module_info.main import ModuleInfo']
    assert m.get_import_strings(use_alias=True) == ['import json', 'import pprint as p', 'from typing import List as l',
                                                    'from json import load', 'from json import dump as d', 'from py_module_info.main import ModuleInfo']


def test_import_string_split(split_test):
    m = ModuleInfo(split_test).get_imports()
    assert m.get_import_strings() == [
        'import json', 'import pprint', 'import types', 'import typing']
    assert m.get_import_strings(use_alias=True) == [
        'import json', 'import pprint', 'import types', 'import typing as t']
