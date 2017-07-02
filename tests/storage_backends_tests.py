# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import shutil
import unittest
import tempfile
from io import BytesIO
from PIL import Image

from flask_thumbnails.storage_backends import FilesystemStorageBackend


class FilesystemStorageBackendTestCase(unittest.TestCase):
    def setUp(self):
        image = Image.new('RGB', (100, 100), 'black')
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        self.tmp_file = tmp_file
        self.backend = FilesystemStorageBackend()

    def test_read(self):
        image = Image.open(BytesIO(self.backend.read(self.tmp_file.name)))
        image.load()
        self.assertEqual(image.size, (100, 100))

    def test_exists(self):
        self.assertTrue(self.backend.exists(os.path.join(os.getcwd(), 'setup.py')))
        self.assertFalse(self.backend.exists(os.path.join(os.getcwd(), 'stup.py')))

    def test_save(self):
        with tempfile.NamedTemporaryFile() as tmp_file:
            self.backend.save(tmp_file.name, b'123')
            self.assertTrue(os.path.exists(tmp_file.name))

    def test_save_with_missing_dir(self):
        directory = tempfile.mkdtemp()
        filepath = os.path.join(directory, 'test_dir/more_test_dir', 'img.jpg')

        try:
            self.assertFalse(os.path.exists(os.path.dirname(filepath)))
            self.backend.save(filepath, b'123')
            self.assertTrue(os.path.exists(os.path.dirname(filepath)))
        finally:
            shutil.rmtree(directory)

    def tearDown(self):
        self.tmp_file.close()
