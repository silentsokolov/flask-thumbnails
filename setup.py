from distutils.core import setup

setup(
    name='Flask-thumbnails',
    version='0.2',
    url='https://github.com/SilentSokolov/flask-thumbnails',
    license='MIT',
    author='Dmitriy Sokolov',
    author_email='silentsokolov@gmail.com',
    description='A simple extension to create a thumbs for the Flask',
    packages=['flask_thumbnails'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'Pillow==2.2.1',
    ],
)
