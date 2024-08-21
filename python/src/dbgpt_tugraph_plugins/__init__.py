"""DB-GPT TuGraph plugins."""

import os
import sys
from pathlib import Path

from dbgpt_tugraph_plugins._version import version

__version__ = version


def get_plugin_binary_path(
    name: str = "leiden",
    system: str = "linux",
    arch: str = "x86_64",
    version: str = "0.1.0",
) -> str:
    """Get plugin binary file path.

    Examples:
        >>> from

    Args:
        name (str): Plugin name. Defaults to "leiden".
        system (str): System name. Defaults to "linux".
        arch (str): Architecture name. Defaults to "x86_64".
        version (str): Plugin version. Defaults to "0.1.0".

    Returns:
        str: Plugin binary file path
    """
    # build the binary file name with version, system and arch
    binary_name = f"{name}-{version}-{system}-{arch}"

    if system == "windows":
        binary_name += ".dll"
    elif system == "darwin":
        binary_name += ".dylib"
    else:
        binary_name += ".so"

    # Get binary file path in the package
    base_dir = Path(__file__).resolve().parent
    binary_path = base_dir / "libs" / binary_name

    if not binary_path.exists():
        raise FileNotFoundError(f"{binary_path} not found.")

    return str(binary_path)


__ALL__ = ["__version__", "get_plugin_binary_path"]
