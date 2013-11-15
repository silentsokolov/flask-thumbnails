import os
import errno
try:
    from PIL import Image, ImageOps
except ImportError:
    raise RuntimeError('Image module of PIL needs to be installed')


class Thumbnail(object):
    def __init__(self, app=None):
        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        self.app = app

        if not self.app.config.get('MEDIA_FOLDER', None):
            raise RuntimeError('You\'re using the flask-thumbnail app '
                               'without having set the required MEDIA_FOLDER setting.')

        if self.app.config.get('MEDIA_THUMBNAIL_FOLDER', None) and not self.app.config.get('MEDIA_THUMBNAIL_URL', None):
            raise RuntimeError('You\'re set MEDIA_THUMBNAIL_FOLDER setting, need set and MEDIA_THUMBNAIL_URL setting.')

        app.config.setdefault('MEDIA_THUMBNAIL_FOLDER', os.path.join(self.app.config['MEDIA_FOLDER'], ''))
        app.config.setdefault('MEDIA_URL', '/')
        app.config.setdefault('MEDIA_THUMBNAIL_URL', os.path.join(self.app.config['MEDIA_URL'], ''))

        app.jinja_env.filters['thumbnail'] = self.thumbnail

    def thumbnail(self, img_url, size, crop=None, bg=None, quality=85):
        """

        :param img_url: url img - '/assets/media/summer.jpg'
        :param size: size return thumb - '100x100'
        :param crop: crop return thumb - 'fit' or None
        :param bg: tuple color or None - (255, 255, 255, 0)
        :param quality: JPEG quality 1-100
        :return: :thumb_url:
        """
        width, height = [int(x) for x in size.split('x')]
        url_path, img_name = os.path.split(img_url)
        name, fm = os.path.splitext(img_name)

        miniature = self._get_name(name, fm, size, crop, bg, quality)

        original_filename = os.path.join(self.app.config['MEDIA_FOLDER'], url_path, img_name)
        thumb_filename = os.path.join(self.app.config['MEDIA_THUMBNAIL_FOLDER'], url_path, miniature)

        # create folders
        self._get_path(thumb_filename)

        thumb_url = os.path.join(self.app.config['MEDIA_THUMBNAIL_URL'], url_path, miniature)

        if os.path.exists(thumb_filename):
            return thumb_url

        elif not os.path.exists(thumb_filename):
            thumb_size = (width, height)
            try:
                image = Image.open(original_filename)
            except IOError:
                return None

            if crop == 'fit':
                img = ImageOps.fit(image, thumb_size, Image.ANTIALIAS)
            else:
                img = image.copy()
                img.thumbnail((width, height), Image.ANTIALIAS)

            if bg:
                img = self._bg_square(img, bg)

            img.save(thumb_filename, image.format, quality=quality)

            return thumb_url

    @staticmethod
    def _bg_square(img, color=0xff):
        size = (max(img.size),) * 2
        layer = Image.new('L', size, color)
        layer.paste(img, tuple(map(lambda x: (x[0] - x[1]) / 2, zip(size, img.size))))
        return layer

    @staticmethod
    def _get_path(full_path):
        directory = os.path.dirname(full_path)

        try:
            if not os.path.exists(full_path):
                os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    @staticmethod
    def _get_name(name, fm, *args):
        for v in args:
            if v:
                name += '_%s' % v
        name += fm

        return name
