import os
from PIL import Image, ImageOps
import errno


class Thumbnail(object):
    def __init__(self, app=None):
        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        # TODO: add default path app directory
        app.config.setdefault('UPLOAD_FOLDER', None)

        app.jinja_env.filters['thumbnail'] = self.thumbnail

    def thumbnail(self, img_url, size, crop=None, bg=None, quality=100):
        """

        :param img_url: url img - '/assets/media/summer.jpg'
        :param size: size return thumb - '100x100'
        :param crop: crop return thumb - 'fit' or None
        :param bg: tuple color or None - (255, 255, 255, 0)
        :param quality: JPEG quality 1-100
        :return: :thumb_url:
        """
        x, y = [int(x) for x in size.split('x')]

        url_path, img_name = os.path.split(img_url)

        img_name, fm = os.path.splitext(img_name)

        miniature = img_name + '_' + size + fm

        original_filename = os.path.join(self.app.config['UPLOAD_FOLDER'], url_path, img_name)
        thumb_filename = os.path.join(self.app.config['UPLOAD_FOLDER'], 'cache', url_path, miniature)

        # create folders
        self._get_path(thumb_filename)

        thumb_url = os.path.join('cache', url_path, miniature)

        if os.path.exists(thumb_filename):
            return thumb_url

        elif not os.path.exists(thumb_filename):
            thumb_size = (x, y)
            try:
                image = Image.open(original_filename)
                #image = image.convert('RGBA')
                if crop == 'fit':
                    size_img = ImageOps.fit(image, thumb_size, Image.ANTIALIAS)
                else:
                    size_img = image.copy()

                if bg:
                    size_img = self._bg_square(size_img, bg)

                size_img.save(thumb_filename, image.format, quality=quality)
                return thumb_url
            except IOError:
                raise IOError

    def _bg_square(self, img, color=0xff):
        size = (max(img.size),) * 2
        layer = Image.new('L', size, color)
        layer.paste(img, tuple(map(lambda x: (x[0] - x[1]) / 2, zip(size, img.size))))
        return layer

    def _get_path(self, full_path):
        directory = os.path.dirname(full_path)

        try:
            if not os.path.exists(full_path):
                os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

