import os
import shutil
import sys

import setuptools
import setuptools.command.build_ext
from setuptools import find_packages, setup

ROOT_DIR = os.path.dirname(__file__)

VERSION = os.environ.get("BUILD_VERSION", "0.1.0")


def _find_bin_files():
    """Find all binary files in libs directory."""
    bin_files = []
    for root, _, filenames in os.walk("libs"):
        for f in filenames:
            if f.endswith(".so") or f.endswith(".dylib") or f.endswith(".dll"):
                bin_files.append(os.path.join(root, f))
    return bin_files


bin_files = _find_bin_files()
print(f"Found binary files: {bin_files}")


def copy_file(target_dir, filename, rootdir):
    source = os.path.relpath(filename, rootdir)
    destination = os.path.join(target_dir, "dbgpt_tugraph_plugins", filename)
    # Create the target directory if it doesn't already exist.
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    if sys.platform == "win32":
        # Does not preserve file mode (needed to avoid read-only bit)
        shutil.copyfile(source, destination, follow_symlinks=True)
    else:
        # Preserves file mode (needed to copy executable bit)
        shutil.copy(source, destination, follow_symlinks=True)
    return 1


def pip_run(build_ext):
    for filename in bin_files:
        copy_file(build_ext.build_lib, filename, ROOT_DIR)
    # Write VERSION file
    version_file = os.path.join(
        build_ext.build_lib, "dbgpt_tugraph_plugins", "_version.py"
    )
    with open(version_file, "w") as f:
        f.write(f'version="{VERSION}"\n')


class build_ext(setuptools.command.build_ext.build_ext):
    def run(self):
        return pip_run(self)


class BinaryDistribution(setuptools.Distribution):
    def has_ext_modules(self):
        return True


setup(
    name="dbgpt-tugraph-plugins",
    version=VERSION,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    cmdclass={"build_ext": build_ext},
    distclass=BinaryDistribution,
    author="",
    author_email="",
    description="TuGraph plugins python package used in DB-GPT.",
    long_description=open("../README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TuGraph-family/dbgpt-tugraph-plugins",
    keywords="TuGraph DB-GPT graph LLM",
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    zip_safe=False,
)
