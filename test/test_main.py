import os

import pytest

from py_module_info import ModuleInfo


@pytest.fixture()
def test_file():
    with open("test_test.py", "w") as f:
        f.write("")
    yield "test_test.py"
    os.remove("test_test.py")


def test_file_not_found_error_raise():
    with pytest.raises(FileNotFoundError):
        m = ModuleInfo("test_test.py")


def test_file_not_found_not_raises(test_file):
    try:
        m = ModuleInfo(test_file)

    except Exception as exc:
        assert False, f"ModuleInfo raised an exception {exc}"
