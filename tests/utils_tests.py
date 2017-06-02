# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest

from flask_thumbnails.utils import import_from_string, generate_filename, parse_size,  aspect_to_string


class UtilsTestCase(unittest.TestCase):
    def test_import_from_string(self):
        c = import_from_string('unittest.TestCase')
        self.assertEqual(c, unittest.TestCase)

    def test_import_from_string_none(self):
        with self.assertRaises(ImportError):
            import_from_string('django.test.NonModel')

    def test_generate_filename(self):
        name = generate_filename('test.jpg', '200x200', 'fit', '100')
        self.assertEqual(name, 'test_200x200_fit_100.jpg')

    def test_parse_size(self):
        size = parse_size('200x200')
        self.assertEqual(size, [200,200])

        size = parse_size('200')
        self.assertEqual(size, [200,200])

        size = parse_size(200)
        self.assertEqual(size, [200,200])

        size = parse_size((200, 200))
        self.assertEqual(size, (200,200))

        size = parse_size((200,))
        self.assertEqual(size, (200,200))

        size = parse_size([200,])
        self.assertEqual(size, [200,200])

    def test_aspect_to_string(self):
        size = aspect_to_string('200x200')
        self.assertEqual(size, '200x200')

        size = aspect_to_string([200,200])
        self.assertEqual(size, '200x200')

        size = aspect_to_string((200,200))
        self.assertEqual(size, '200x200')
