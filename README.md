# Py Module Info

[![Testing](https://github.com/Adwaith-Rajesh/py-module-info/actions/workflows/tests.yml/badge.svg)](https://github.com/Adwaith-Rajesh/py-module-info/actions/workflows/tests.yml)

Get extra info about a python module, like imports, functions called inside other funcs etc.

___
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
