# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest

from flask_thumbnails.utils import import_from_string, generate_filename


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


if __name__ == '__main__':
    unittest.main()
