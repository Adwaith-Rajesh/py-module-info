import ast
from pathlib import Path
from typing import Dict
from typing import List
from typing import Union

from ._core import find_function_def_in_class_def
from ._core import get_func_meta_data
from ._core import get_imports

__all__ = ("get_ast", "ModuleInfo")


def read_file_code(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def get_ast(filename: str) -> ast.Module:
    return ast.parse(read_file_code(filename))


class Imports:

    def __init__(self, imports: List[Union[ast.Import, ast.ImportFrom]]) -> None:
        self._imports = imports

    def get_imported_names(self, use_alias=False) -> List[str]:
        """
        from typing import List -> List
        if use_alias:
            from typing import List as l -> l
        else:
            list
        """

        i_names = []
        for i in self._imports:
            for alias in i.names:
                if use_alias:
                    i_names.append(self.__get_alias(alias))
                else:
                    i_names.append(alias.name)

        return i_names

    def get_import_strings(self, use_alias=False) -> List[str]:
        """Convet import ast to import strings
        The ast of the import string:
            import one, two
        after converting it from ast to string again will be
            import one
            import two
        """
        import_strings = []

        for i in self._imports:
            if isinstance(i, ast.Import):
                for alias in i.names:
                    if use_alias:
                        # the alias name of the import does not exists
                        if alias.name == self.__get_alias(alias):
                            import_strings.append(f"import {alias.name}")
                        else:
                            import_strings.append(
                                f"import {alias.name} as {self.__get_alias(alias)}")
                    else:
                        import_strings.append(f"import {alias.name}")
            elif isinstance(i, ast.ImportFrom):
                for alias in i.names:
                    if use_alias:
                        # the alias name of the import does not exists
                        if alias.name == self.__get_alias(alias):
                            import_strings.append(
                                f"from {i.module} import {alias.name}")
                        else:
                            import_strings.append(
                                f"from {i.module} import {alias.name} as {self.__get_alias(alias)}")
                    else:
                        import_strings.append(
                            f"from {i.module} import {alias.name}")

        return import_strings

    def __get_alias(self, al: ast.alias) -> str:
        """Return the asname of ast.alias if it exists """
        if al.asname is not None:
            return al.asname
        else:
            return al.name


class ModuleInfo:

    def __init__(self, filename: str) -> None:
        self.filename = filename

        if not Path(self.filename).is_file():
            raise FileNotFoundError(f"File {self.filename!r} does not exists")

        self._tree = get_ast(self.filename)

    def get_imports(self) -> Imports:
        return Imports(get_imports(self._tree))

    def get_funcs_info(self, only_func_names: bool = False) -> Dict[str, List[ast.Call]]:
        """Return a list of all the func call that are executed inside the funcs
        Example:
            def foo():
                with open("test.json", "r") as f:
                    load(f)
            the function when called for get_func_call_in_func will return ast.Call object of open, load
        """

        func_info = {}

        tree = find_function_def_in_class_def(self._tree)
        for child in ast.walk(tree):
            if isinstance(child, ast.FunctionDef):
                if not hasattr(child, "parent"):
                    func_info[child.name] = get_func_meta_data(
                        child,  read_file_code(self.filename), only_func_names)

        return func_info

    def get_classes_info(self) -> Dict[str, List[ast.Call]]:
        pass
