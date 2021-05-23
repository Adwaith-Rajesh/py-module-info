import ast
from typing import List
from typing import Union


def get_imports(tree: ast.Module) -> List[Union[ast.ImportFrom, ast.Import]]:

    imports = []
    for child in ast.walk(tree):
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            imports.append(child)

    return imports
