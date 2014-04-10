import os
import unittest

import flask
from flask.ext.thumbnails import Thumbnail


class ThumbnailTestCase(unittest.TestCase):

    def setUp(self):
        app = flask.Flask(__name__)
        app.config['TESTING'] = True
        app.config['MEDIA_FOLDER'] = '/tmp/thumbnail'
        app.config['MEDIA_URL'] = '/uploads/'
        self.thumb = Thumbnail(app)

    def test_create_missing_path(self):
        self.assertFalse(os.path.exists('/tmp/thumbnail/media/test/subtest/'))
        self.thumb._get_path('/tmp/thumbnail/media/test/subtest/test.jpg')
        self.assertTrue(os.path.exists('/tmp/thumbnail/media/test/subtest/'))
        os.removedirs('/tmp/thumbnail/media/test/subtest/')

    def test_create_thumb_name(self):
        name = self.thumb._get_name('test', '.jpg', '200x200', 'fit', '100')
        self.assertEquals(name, 'test_200x200_fit_100.jpg')

        name = self.thumb._get_name('test', '.jpg')
        self.assertEquals(name, 'test.jpg')

        name = self.thumb._get_name('test', '.jpg', 100)
        self.assertEquals(name, 'test_100.jpg')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()