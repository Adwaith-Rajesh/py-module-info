import ast
from typing import Any
from typing import Dict
from typing import List
from typing import Union


def get_imports(tree: ast.Module) -> List[Union[ast.ImportFrom, ast.Import]]:

    imports = []
    for child in ast.walk(tree):
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            imports.append(child)

    return imports


def get_calls(func: ast.FunctionDef, code: str, end_calls_only: bool = False) -> List[str]:
    calls = []
    if not end_calls_only:
        # return the entire call string
        for child in ast.walk(func):
            if isinstance(child, ast.Call):
                calls.append(ast.get_source_segment(code, child))

    else:
        # return just the name of the function that was called
        for child in ast.walk(func):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    calls.append(child.func.id)

                elif isinstance(child.func, ast.Attribute):
                    calls.append(child.func.attr)

    calls = list(set(calls))
    calls.sort()
    return calls  # easy way to remove duplicates


def get_func_meta_data(func: ast.FunctionDef, code: str, only_func_names: bool = False) -> Dict[str, Union[int, List[str]]]:
    """
    Get the numbers of argument passed, the name of the arguments.. etc
    """
    meta_data: Dict[str, List[str]] = {}
    if isinstance(func, ast.FunctionDef):
        meta_data["args"] = [arg.arg for arg in func.args.args]
        meta_data["defaults"] = [d.value for d in func.args.defaults]
        meta_data["arg_count"] = len(meta_data["args"])  # this is an int
        meta_data["calls"] = get_calls(func, code, only_func_names)

    return meta_data


def find_function_def_in_class_def(tree: ast.Module) -> ast.Module:
    """adds an attribute parent to the ast.FunctionDef in ClassDef
    so that it can be uniquely identified as methods in ClassDef
    """

    for child in ast.walk(tree):
        if isinstance(child, ast.ClassDef):
            for sub_child in ast.walk(child):
                if isinstance(sub_child, ast.FunctionDef):
                    sub_child.parent = child.name

    return tree
