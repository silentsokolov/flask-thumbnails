from distutils.core import setup

setup(
    name='Flask-thumbnails',
    version='0.1',
    url='',
    license='MIT',
    author='silent',
    author_email='silentsokolov@gmail.com',
    description='A simple extension to create a thumbs for the flask',
    py_modules=['flask_thumbnails'],
    # packages=['flask_thumbnails'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'Pillow',
    ],
)
