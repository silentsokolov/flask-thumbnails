# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import importlib


def import_from_string(path):
    path_bits = path.split('.')
    class_name = path_bits.pop()
    module_path = '.'.join(path_bits)
    module_itself = importlib.import_module(module_path)

    if not hasattr(module_itself, class_name):
        raise ImportError('The Python module \'%s\' has no \'%s\' class.' % (module_path, class_name))

    return getattr(module_itself, class_name)


def generate_filename(original_filename, *options):
    name, ext = os.path.splitext(original_filename)
    for v in options:
        if v:
            name += '_%s' % v
    name += ext

    return name
