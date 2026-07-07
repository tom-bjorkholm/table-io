#! /usr/local/bin/python3
"""Setup file specifying build of .whl."""

from setuptools import setup

setup(
  name='tableio',
  version='1.1.1',
  description='Uniform way to write table data to and read from different ' \
    'file formats',
  author='Tom Björkholm',
  author_email='klausuler_linnet0q@icloud.com',
  python_requires='>=3.12',
  packages=['tableio'],
  package_dir={'tableio': 'src/tableio'},
  package_data={'tableio': ['src/py.typed']},
  install_requires=[
    'mformat-ext >= 0.7',
    'openpyxl >= 3.1.5',
    'types-openpyxl >= 3.1.5.20260518',
    'odfdo >= 3.22.10',
    'xlsxwriter >= 3.2.9',
    'pylightxl >= 1.61'
  ]
)
