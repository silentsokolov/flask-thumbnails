#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
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
    author='Dmitriy Sokolov',
    author_email='silentsokolov@gmail.com',
    description='A simple extension to create a thumbs for the Flask',
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    test_suite='tests',
    packages=get_packages('flask_thumbnails'),
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
