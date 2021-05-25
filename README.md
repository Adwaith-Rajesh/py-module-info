# Py Module Info

[![Testing](https://github.com/Adwaith-Rajesh/py-module-info/actions/workflows/tests.yml/badge.svg)](https://github.com/Adwaith-Rajesh/py-module-info/actions/workflows/tests.yml)
[![Upload Python Package](https://github.com/Adwaith-Rajesh/py-module-info/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Adwaith-Rajesh/py-module-info/actions/workflows/python-publish.yml)

Get extra info about a python module, like imports, functions called inside other funcs etc.
___

## Installation
```bash
pip install py-module-info
```

## Why use this?
Well Idk, the `inspect` module in python requires you to import the module.
This package does not require you to import, but rather just looks at the python file like a normal text file and parses it. The problem with importing is that it may execute code that can harm your PC. So maybe ?


## What does it do?

### Get info about the imports used

```python
# test.py

import json
import pprint as p
from typing import List as l
from json import load, dump as d
from py_module_info.main import ModuleInfo
```
To get the imported names use

```python
from py_module_info import ModuleInfo
m = ModuleInfo("test.py")
imports = m.get_imports()
print(imports.get_imported_names())

# output
['json', 'pprint', 'List', 'load', 'dump', 'ModuleInfo']

# in order to get the alias names used
print(imports.get_imported_names(use_alias=True))
# output
['json', 'p', 'l', 'load', 'd', 'ModuleInfo']
```

To get the literal import string in the module use

```python
from py_module_info import ModuleInfo
m = ModuleInfo("test.py")
imports = m.get_imports()
print(imports.get_import_strings())

# output
['import json', 'import pprint', 'from typing import List',
'from json import load', 'from json import dump', 'from py_module_info.main import ModuleInfo']

# use alias names insted
print(imports.get_import_strings(use_alias=True))

# output
['import json', 'import pprint as p', 'from typing import List as l',
'from json import load', 'from json import dump as d', 'from py_module_info.main import ModuleInfo']
```
#### Note
 * The imports will be split into individual imports:
```python
 import test, json
```
* will become
```python
import test
import json
```

### Get info about the function in the module.

```python
# test.py

import json
from pprint import pprint

def foo():
    pprint({"Hello": "World"})


    with open("test.json") as f:
        print(json.load(f))
```

To get info about the functions use
```python
from py_module_info import ModuleInfo

m = ModuleInfo("test.py")
print(m.get_funcs_info())

# output
{'foo': {'args': [], 'defaults': [], 'arg_count': 0, 'calls': ['json.load(f)', 'open("test.json")', 'pprint({"Hello": "World"})', 'print(json.load(f))']}}

```
The output includes the args passed in function, the defaults value for the the arguments, the argument count, and all the function calls that happened inside the function.

The function calls are all expanded and includes the entire call string.

In order to get just the function calls use

```python
from py_module_info import ModuleInfo

m = ModuleInfo("test.py")
print(m.get_funcs_info(only_func_name=True))

# output
{'foo': {'args': [], 'defaults': [], 'arg_count': 0, 'calls': ['load', 'open', 'pprint', 'print']}}

```