# tableio

> **👤 Looking to use this in your program**  
> This repository is for developers of the package. If you want to install
> and use `tableio` including writing programs that use them, please visit
> the **PyPI project page [https://pypi.org/project/tableio](https://pypi.org/project/tableio)
> for installation instructions and user documentation.

## What is it

The tableio package contains a number of classes providing a uniform way for
a python program to write table data (rows of columns) to and read table data
from a number of different common file formats.

The primary intended use is for text output from a python program, where the
programmer would like the user to be able to select the input and output file
formats.

The support for spreadsheets is for reading and writing data. There is no
intention to support reading or writing formulas. There is no support for
running calculations in the spreadsheets (although nothing will stop a
receiver of a spreadsheet created by tableio package to manually add
formulas in the received spreadsheet).

## For developers

### Cloning

The tableio repo uses submodules. To clone it use the command:

````sh
git clone --recurse-submodules git@github.com:tom-bjorkholm/table-io.git
````

If you forgot to include the `--recurse-submodules` in your `git clone` command
you can fix it later with the command:

````sh
git submodule update --init --recursive 
````

To update the version of thr submodule repo that you see in the main repo use the command:

````sh
git submodule update --remote --merge
````

### Needed environment

#### OS

For running the script and running the test suite you need a mac or a Linux computer.
Even if the resulting package can be installed and used on Windows, the scripts for
building and testing are only implemented for mac and Linux.

#### Python version

Please see README_pypi.md for information on needed python version.
Main development is on newest Python version.

### Quick start

1. Clone this repository
2. Run `./run_setup_build_environment.py` to set up the build environment
3. Run `./run_build.py`  to build and test the package

### Building application

There are 3 main scripts (and 2 extra convinience scripts) for building the application:

- `run_setup_build_environment.py` Run this script first to get the
  environment set up for building.
- `run_build.py` Run this script to build an installation package (.whl) and
  to run the tests on it in a venv (virtual environment).
- `run_clean.py` Deletes all files that was produced by the build to start
  over from a clean state.
- `run_clean_build.py` Combines the use of `run_clean.py`,
  `run_setup_build_environment.py` and `run_build.py` into one script.
  Pylint discover some duplicate code warnings only on a clean build so this
  is useful.
- `run_pypi_build.py` Builds for PyPI upload and can do the upload too.

The "testing" includes pytest, pylint, flake8 and mypy.

After running `run_build.py` you can open `reports/index.html` to see all test
reports.

### More build system information

The file `./common_build_tools/README.md` (in git submodule - see above) contains more
information about the build system. This README can also be viewed at
[https://github.com/tom-bjorkholm/common_build_tools/blob/master/README.md](https://github.com/tom-bjorkholm/common_build_tools/blob/master/README.md)

## Test summary

- Test result: 1347 passed in 20s
- No flake8 warnings.
- No mypy errors found.
- No python layout warnings.
- Built version(s): 1.1.1
- Build and test using Python 3.14.6
