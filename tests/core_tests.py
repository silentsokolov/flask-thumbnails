# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import tempfile
import unittest
from io import BytesIO

import mock
from flask import Flask
from PIL import Image

from flask_thumbnails import Thumbnail
from flask_thumbnails.storage_backends import FilesystemStorageBackend


class CoreTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.thumbnail = Thumbnail(app=self.app)
        self.client = self.app.test_client()

        self.image = Image.new("RGB", (100, 100), "black")

    def test_root_directory(self):
        self.app.config["THUMBNAIL_MEDIA_ROOT"] = "media"
        self.assertEqual(
            self.thumbnail.root_directory,
            os.path.join(self.app.root_path, self.app.config["THUMBNAIL_MEDIA_ROOT"]),
        )

        self.app.config["THUMBNAIL_MEDIA_ROOT"] = "/tmp/media"
        self.assertEqual(self.thumbnail.root_directory, self.app.config["THUMBNAIL_MEDIA_ROOT"])

    def test_thumbnail_directory(self):
        self.app.config["THUMBNAIL_MEDIA_THUMBNAIL_ROOT"] = "media"
        self.assertEqual(
            self.thumbnail.thumbnail_directory,
            os.path.join(self.app.root_path, self.app.config["THUMBNAIL_MEDIA_THUMBNAIL_ROOT"]),
        )

        self.app.config["THUMBNAIL_MEDIA_THUMBNAIL_ROOT"] = "/tmp/media"
        self.assertEqual(
            self.thumbnail.thumbnail_directory,
            self.app.config["THUMBNAIL_MEDIA_THUMBNAIL_ROOT"],
        )

    def test_root_url(self):
        self.app.config["THUMBNAIL_MEDIA_URL"] = "/media"
        self.assertEqual(self.thumbnail.root_url, self.app.config["THUMBNAIL_MEDIA_URL"])

    def test_thumbnail_url(self):
        self.app.config["THUMBNAIL_MEDIA_THUMBNAIL_URL"] = "/media"
        self.assertEqual(
            self.thumbnail.thumbnail_url,
            self.app.config["THUMBNAIL_MEDIA_THUMBNAIL_URL"],
        )

    def test_storage_backend(self):
        self.assertEqual(
            self.thumbnail.storage_backend, self.app.config["THUMBNAIL_STORAGE_BACKEND"]
        )

    def test_get_storage_backend(self):
        self.assertIsInstance(self.thumbnail.get_storage_backend(), FilesystemStorageBackend)

    def test_colormode(self):
        image = Image.new("L", (10, 10))
        new_image = self.thumbnail.colormode(image)

        self.assertEqual(new_image.mode, "RGB")

        image = Image.new("LA", (10, 10))
        new_image = self.thumbnail.colormode(image)

        self.assertEqual(new_image.mode, "RGBA")

        image = Image.new("RGBA", (10, 10))
        new_image = self.thumbnail.colormode(image)

        self.assertEqual(new_image.mode, "RGBA")

        image = Image.new("RGB", (10, 10))
        new_image = self.thumbnail.colormode(image)

        self.assertEqual(new_image.mode, "RGB")

    def test_get_format(self):
        image = Image.new("RGB", (10, 10))
        new_image = self.thumbnail.colormode(image)

        self.assertEqual(new_image.mode, "RGB")

        options = {"format": "PNG"}
        self.assertEqual(
            self.thumbnail._get_format(image, **options), "PNG"  # pylint: disable=protected-access
        )

        options = {}
        self.assertEqual(
            self.thumbnail._get_format(image, **options),  # pylint: disable=protected-access
            self.app.config["THUMBNAIL_DEFAULT_FORMAT"],
        )

    def test_get_raw_data(self):
        image = Image.new("L", (10, 10))

        options = {"format": "JPEG"}
        data = self.thumbnail.get_raw_data(image, **options)

        new_image = Image.open(BytesIO(data))
        self.assertEqual(image.mode, new_image.mode)
        self.assertEqual(image.size, new_image.size)
        self.assertEqual(new_image.format, "JPEG")

    def test_create_thumbnail(self):
        image = Image.new("L", (100, 100))

        new_image = self.thumbnail._create_thumbnail(  # pylint: disable=protected-access
            image, size=(50, 50)
        )

        self.assertEqual(new_image.size, (50, 50))

        new_image = self.thumbnail._create_thumbnail(  # pylint: disable=protected-access
            image, size=(50, 50), crop=None
        )

        self.assertEqual(new_image.size, (50, 50))

    @mock.patch("flask_thumbnails.utils.generate_filename")
    def test_get_thumbnail(self, mock_thumb_name):
        with tempfile.NamedTemporaryFile(suffix=".jpg") as original:
            with tempfile.NamedTemporaryFile(suffix=".jpg") as thumb:
                mock_thumb_name.return_value = os.path.basename(thumb.name)
                self.app.config["THUMBNAIL_MEDIA_ROOT"] = os.path.dirname(original.name)
                self.app.config["THUMBNAIL_MEDIA_THUMBNAIL_ROOT"] = os.path.dirname(thumb.name)

                image = Image.new("RGB", (100, 100), "black")
                image.save(original.name)

                thumb_url = self.thumbnail.get_thumbnail(os.path.basename(original.name), "200x200")

                self.assertTrue(thumb_url)
