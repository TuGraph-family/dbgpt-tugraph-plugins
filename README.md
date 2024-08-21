# dbgpt-tugraph-plugins

TuGraph plugins python package used in DB-GPT.

## Why this repository?

TuGraph plugins are written in cpp and are compiled into dynamic link libraries. The purpose of this repository is to package these plugins into a python package so that they can be easily installed and used in DB-GPT.


## How to use in python?

1. First install the package using pip:

```bash
pip install dbgpt-tugraph-plugins>=0.1.0rc1 -U -i https://pypi.org/simple
```

2. Then you can use the plugins in python:

```python
from dbgpt_tugraph_plugins import get_plugin_binary_path

leiden_bin_abs_path = get_plugin_binary_path("leiden") 

print(leiden_bin_abs_path)
```

You will get the absolute path to the leiden plugin binary file.


## How to build the package?

```bash
BUILD_VERSION=0.1.0rc1 make py-package
```

The package will be built in the `python/dist` directory.
