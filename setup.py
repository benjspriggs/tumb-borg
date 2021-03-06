#!/usr/bin/python

from setuptools import setup
setup(name='tumb-borg',
    version='0.2',
    author='Benjamin Spriggs',
    author_email='benjspriggs@sprico.com',
    license='Apache 3.0',
    description='Simple poetry uploader.',
    install_requires = [
        'python-tumblpy',
        'pyyaml'
        ],
    py_modules=['tumb_borg'])
