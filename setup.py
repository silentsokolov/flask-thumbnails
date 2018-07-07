#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from os.path import join, dirname
from setuptools import setup


def get_version(package):
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    return [dirpath for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


setup(
    name='Flask-thumbnails',
    version=get_version('flask_thumbnails'),
    url='https://github.com/silentsokolov/flask-thumbnails',
    license='MIT',
    description='A simple extension to create a thumbs for the Flask',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author='Dmitriy Sokolov',
    author_email='silentsokolov@gmail.com',
    packages=get_packages('flask_thumbnails'),
    include_package_data=True,
    install_requires=[],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    zip_safe=False,
    platforms='any',
    test_suite='tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ]
)
