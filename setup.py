#! /usr/local/bin/python3
"""Setup file specifying build of .whl."""

from setuptools import setup

setup(
  name='tableio',
  version='1.3.1',
  description='Uniform way to write table data to and read from different ' \
    'file formats',
  author='Tom Björkholm',
  author_email='klausuler_linnet0q@icloud.com',
  python_requires='>=3.12',
  packages=['tableio'],
  package_dir={'tableio': 'src/tableio'},
  package_data={'tableio': ['src/py.typed']},
  install_requires=[
    'mformat-ext >= 0.8',
    'openpyxl >= 3.1.5',
    'types-openpyxl >= 3.1.5.20261017',
    'odfdo >= 3.27.3',
    'xlsxwriter >= 3.3.0',
    'pylightxl >= 1.61'
  ]
)
