# -*- coding: utf-8 -*-
import importlib
import os


def import_from_string(path):
    path_bits = path.split(".")
    class_name = path_bits.pop()
    module_path = ".".join(path_bits)
    module_itself = importlib.import_module(module_path)

    if not hasattr(module_itself, class_name):
        raise ImportError(
            f"The Python module '{module_path}' has no '{class_name}' class."
        )

    return getattr(module_itself, class_name)


def generate_filename(original_filename, *options, extension=None):
    name, ext = os.path.splitext(original_filename)
    if extension:
        ext = extension
    return f"{name}_{'_'.join(options)}{ext}"


def parse_size(size):
    if isinstance(size, int):
        # If the size parameter is a single number, assume square aspect.
        return [size, size]

    if isinstance(size, (tuple, list)):
        return size + tuple(size) if len(size) == 1 else size[:2]

    try:
        thumbnail_size = [int(x) for x in size.lower().split("x", 1)]
    except ValueError as e:
        raise ValueError("Bad thumbnail size format. Valid format is INTxINT.") from e

    if len(thumbnail_size) == 1:
        # If the size parameter only contains a single integer, assume square aspect.
        thumbnail_size.append(thumbnail_size[0])

    return thumbnail_size


def aspect_to_string(size):
    return size if isinstance(size, str) else "x".join(map(str, size))
