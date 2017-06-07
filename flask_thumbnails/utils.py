# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys
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


def parse_size(size):
    if sys.version_info < (3,):
        integer_types = (int, long)
    else:
        integer_types = (int,)

    if isinstance(size, integer_types):
        # If the size parameter is a single number, assume square aspect.
        return [size, size]

    if isinstance(size, (tuple, list)):
        if len(size) == 1:
            # If single value tuple/list is provided, exand it to two elements
            return size + type(size)(size)
        return size

    try:
        thumbnail_size = [int(x) for x in size.lower().split('x', 1)]
    except ValueError:
        raise ValueError('Bad thumbnail size format. Valid format is INTxINT.')

    if len(thumbnail_size) == 1:
        # If the size parameter only contains a single integer, assume square aspect.
        thumbnail_size.append(thumbnail_size[0])

    return thumbnail_size


def aspect_to_string(size):
    if sys.version_info < (3,):
        str_type = basestring
    else:
        str_type = str

    if isinstance(size, str_type):
        return size

    return 'x'.join(map(str, size))
