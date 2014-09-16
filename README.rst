.. image:: https://travis-ci.org/silentsokolov/flask-thumbnails.png?branch=master
   :target: https://travis-ci.org/silentsokolov/flask-thumbnails

flask-thumbnails
================

A simple extension to create a thumbs for the Flask


Installation
------------

Install with ``pip``:

Run ``pip install git+https://github.com/SilentSokolov/flask-thumbnails.git``

Add ``Thumbnail`` to your extension file:

.. code:: python

    from flask.ext.thumbnails import Thumbnail

    app = Flask(__name__)

    thumb = Thumbnail(app)

Add ``MEDIA_FOLDER`` and ``MEDIA_URL`` in your settings:

.. code:: python

    app.config['MEDIA_FOLDER'] = '/home/www/media'
    app.config['MEDIA_URL'] = '/media/'


Example usage
-------------

Use in Jinja2 template:

::

    <img src="{{ 'image.jpg'|thumbnail('200x200') }}" alt="" />
    <img src="{{ 'image.jpg'|thumbnail('200x200', crop='fit', quality=100) }}" alt="" />


Options
~~~~~~~

``crop='fit'`` returns a sized and cropped version of the image, cropped to the requested aspect ratio and size, `read more <http://pillow.readthedocs.org/en/latest/reference/ImageOps.html#PIL.ImageOps.fit>`_.

``quality=XX`` changes the quality of the output JPEG thumbnail, default ``85``.


Develop and Production
----------------------

Production
~~~~~~~~~~

In production, you need to add media directory in you web server.


Develop
~~~~~~~

To service the uploaded files need a helper function, where ``/media/`` your settings ``app.config['MEDIA_URL']``:

.. code:: python

    from flask import send_from_directory

    @app.route('/media/<regex("([\w\d_/-]+)?.(?:jpe?g|gif|png)"):filename>')
    def media_file(filename):
        return send_from_directory(app.config['MEDIA_THUMBNAIL_FOLDER'], filename)


Option settings
---------------

If you want to store the thumbnail in a folder other than the ``MEDIA_FOLDER``, you need to set it manually:

.. code:: python

    app.config['MEDIA_THUMBNAIL_FOLDER'] = '/home/www/media/cache'
    app.config['MEDIA_THUMBNAIL_URL'] = '/media/cache/'
