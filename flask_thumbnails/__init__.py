# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from io import BytesIO

try:
    from PIL import Image, ImageOps
except ImportError:
    raise RuntimeError('Get Pillow at https://pypi.python.org/pypi/Pillow '
                       'or run command "pip install Pillow".')

from .utils import import_from_string, generate_filename, parse_size, aspect_to_string

__version__ = '1.0.1'


class Thumbnail(object):
    def __init__(self, app=None, configure_jinja=True):
        self.app = app
        self._configure_jinja = configure_jinja
        self._default_root_directory = 'media'
        self._default_thumbnail_directory = 'media'
        self._default_root_url = '/'
        self._default_thumbnail_root_url = '/'
        self._default_format = 'JPEG'
        self._default_storage_backend = 'flask_thumbnails.storage_backends.FilesystemStorageBackend'

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if self.app is None:
            self.app = app
        app.thumbnail_instance = self

        if not hasattr(app, 'extensions'):
            app.extensions = {}

        if 'thumbnail' in app.extensions:
            raise RuntimeError('Flask-thumbnail extension already initialized')

        app.extensions['thumbnail'] = self

        app.config.setdefault('THUMBNAIL_MEDIA_ROOT', self._default_root_directory)
        app.config.setdefault('THUMBNAIL_MEDIA_THUMBNAIL_ROOT', self._default_thumbnail_directory)
        app.config.setdefault('THUMBNAIL_MEDIA_URL', self._default_root_url)
        app.config.setdefault('THUMBNAIL_MEDIA_THUMBNAIL_URL', self._default_thumbnail_root_url)
        app.config.setdefault('THUMBNAIL_STORAGE_BACKEND', self._default_storage_backend)
        app.config.setdefault('THUMBNAIL_DEFAUL_FORMAT', self._default_format)

        if self._configure_jinja:
            app.jinja_env.filters.update(
                thumbnail=self.get_thumbnail,
            )

    @property
    def root_directory(self):
        path = self.app.config['THUMBNAIL_MEDIA_ROOT']

        if os.path.isabs(path):
            return path
        else:
            return os.path.join(self.app.root_path, path)

    @property
    def thumbnail_directory(self):
        path = self.app.config['THUMBNAIL_MEDIA_THUMBNAIL_ROOT']

        if os.path.isabs(path):
            return path
        else:
            return os.path.join(self.app.root_path, path)

    @property
    def root_url(self):
        return self.app.config['THUMBNAIL_MEDIA_URL']

    @property
    def thumbnail_url(self):
        return self.app.config['THUMBNAIL_MEDIA_THUMBNAIL_URL']

    @property
    def storage_backend(self):
        return self.app.config['THUMBNAIL_STORAGE_BACKEND']

    def get_storage_backend(self):
        backend_class = import_from_string(self.storage_backend)
        return backend_class(app=self.app)

    def get_thumbnail(self, original, size, **options):
        storage = self.get_storage_backend()
        crop = options.get('crop', 'fit')
        background = options.get('background')
        quality = options.get('quality', 90)
        thumbnail_size = parse_size(size)

        original_path, original_filename = os.path.split(original)
        thumbnail_filename = generate_filename(original_filename, aspect_to_string(size), crop, background, quality)

        original_filepath = os.path.join(self.root_directory, original_path, original_filename)
        thumbnail_filepath = os.path.join(self.thumbnail_directory, original_path, thumbnail_filename)
        thumbnail_url = os.path.join(self.thumbnail_url, original_path, thumbnail_filename)

        if storage.exists(thumbnail_filepath):
            return thumbnail_url

        image = Image.open(BytesIO(storage.read(original_filepath)))
        try:
            image.load()
        except (IOError, OSError):
            self.app.logger.warning('Thumbnail not load image: %s', original_filepath)
            return thumbnail_url

        image = self._create_thumbnail(image, thumbnail_size, crop)

        raw_data = self.get_raw_data(image, **options)
        storage.save(thumbnail_filepath, raw_data)

        return thumbnail_url

    def get_raw_data(self, image, **options):
        data = {
            'format': self._get_format(image, **options),
            'quality': options.get('quality', 90),
        }

        _file = BytesIO()
        image.save(_file, **data)
        return _file.getvalue()

    @staticmethod
    def colormode(image, colormode='RGB'):
        if colormode == 'RGB':
            if image.mode == 'RGBA':
                return image
            if image.mode == 'LA':
                return image.convert('RGBA')
            return image.convert(colormode)

        if colormode == 'GRAY':
            return image.convert('L')

        return image.convert(colormode)

    @staticmethod
    def background(original_image, color=0xff):
        size = (max(original_image.size),) * 2
        image = Image.new('L', size, color)
        image.paste(original_image, tuple(map(lambda x: (x[0] - x[1]) / 2, zip(size, original_image.size))))

        return image

    def _get_format(self, image, **options):
        if options.get('format'):
            return options.get('format')
        if image.format:
            return image.format

        return self.app.config['THUMBNAIL_DEFAUL_FORMAT']

    def _create_thumbnail(self, image, size, crop='fit', background=None):
        if crop == 'fit':
            image = ImageOps.fit(image, size, Image.ANTIALIAS)
        else:
            image = image.copy()
            image.thumbnail(size, resample=Image.ANTIALIAS)

        if background is not None:
            image = self.background(image)

        image = self.colormode(image)

        return image
