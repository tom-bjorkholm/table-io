# mformat

> **👤 Looking to use this in your program**  
> This repository is for developers of the package. If you want to install and use `mformat` or `mformat-ext` including writing programs that use them, please visit the **PyPI project page [https://pypi.org/project/mformat](https://pypi.org/project/mformat) or [https://pypi.org/project/mformat-ext](https://pypi.org/project/mformat-ext)** for installation instructions and user documentation.

## What is it

The mformat package contains a number of classes providing a uniform way for a python program to write to a number of different file formats.

The primary intended use is for text output from a python program, where the programmer would like the user to be able to select the output file formats. Some users may want the text as a Microsoft Word file, others as a LibreOffice Open Document Text file, while still others might want it as Markdown. By using the uniform way of writing provided by mformat the same python code can produce output in a number of different formats.

This is intended to provide an easy and uniform way to produce information in different formats. The emphasis is on getting the same information into the different formats. This will allow you to get a correct (but perhaps rudimentary) document in several formats. If you want to produce the most estetically pleasing document in a particular format, this is not the correct library to use.

### mformat base package

The base package contains support for the output formats that are supported with a minimum of dependencies. The base folder contains the source code and tests of the base package.

### mformat-ext extended package

The extended package contains also support for additional output formats that require additional dependencies. The extend folder contains the source code and tests of the extended package.

### Examples

To make it easy for a programmer new to mformat to start using it there are a number of example programs. The example folder contains the example programs, as well as the output produced by running the example programs. There is currently very few tests of the example programs in the automatic test suite.

## For developers

### Cloning

The mformat repo uses submodules. To clone it use the command:

````sh
git clone --recurse-submodules git@bitbucket.org:tom-bjorkholm/mformat.git
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

For running the script and running the test suite you need a mac or a Linux computer. Even if the resulting package can be installed and used on Windows, the scripts for building and testing are only implemented for mac and Linux.

#### Python version

Please see README_pypi.md for information on needed python version. Main development is on newest Python version.

#### Zsh

The scripts are all zsh. zsh is available by default on modern macs. zsh can easily be installed on Linux (on Ubuntu: `sudo apt install zsh`).

### Quick start

1. Clone this repository
2. Run `./setup_build_environment.zsh` to set up the build environment
3. Run `./doBuild.zsh` to build and test the package

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
[https://bitbucket.org/tom-bjorkholm/common_build_tools/src/master/README.md](https://bitbucket.org/tom-bjorkholm/common_build_tools/src/master/README.md)

### The readme files for PyPI

The script `build_helpers/create_pypi_readme.py` creates the 2 readme files for PyPI:
`base/README_pypi.md` and `extend/README_pypi.org`.

## Test summary

- Test result: 2 failed, 139 passed in 5s
- Flake8 errors/warnings.
- No mypy errors found.
- Built version(s): 0.0.1
- Build and test using Python 3.14.3
