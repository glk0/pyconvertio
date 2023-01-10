#!/usr/bin/env python3

import os
from setuptools import setup

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup (
    name='pyconvertio',
    version='0.0.0',
    description='Lightweight Python wrapper for the Convertio  API',
    author='Kossi GLOKPOR',
    license='Unlicense',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages = ["pyconvertio"],
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License"
    ],
    install_requires=['requests', 'validators'],
    python_requires='>=3.8',
    include_package_data=True
)
