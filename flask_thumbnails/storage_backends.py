# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os


class BaseStorageBackend(object):
    def __init__(self, app=None):
        self.app = app

    def read(self, filepath, **kwargs):
        raise NotImplementedError

    def exists(self, filepath):
        raise NotImplementedError

    def save(self, filepath, data):
        raise NotImplementedError


class FilesystemStorageBackend(BaseStorageBackend):
    def read(self, filepath, mode='rb'):
        with open(filepath, mode) as f:
            return f.read()

    def exists(self, name):
        return os.path.exists(name)

    def save(self, filepath, data):
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'wb') as f:
            f.write(data)
