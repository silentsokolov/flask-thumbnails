Flask-thumbnails
================

A simple extension to create a thumbs for the flask

## Installation

Install with ``pip``:

    pip install git+https://github.com/SilentSokolov/flask-thumbnails.git

Install:

    from flask.ext.thumbnails import Thumbnail

    app = Flask(__name__)

    thumb = Thumbnail(app)

Add ``UPLOAD_FOLDER`` in your settings:

    UPLOAD_FOLDER = '/home/www/media'

Use in Jinja2 template:

    {{ 'sc.jpg'|thumbnail('200x200') }}
    {{ object_img|thumbnail('200x200', crop='fit') }}