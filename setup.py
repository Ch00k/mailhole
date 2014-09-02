#!/usr/bin/env python

from setuptools import setup
from mailhole import __version__


setup(
    name = 'mailhole',
    version=__version__,
    description = 'Fake SMTP server, used for testing',
    author = 'Andriy Yurchuk',
    author_email = 'ayurchuk@minuteware.net',
    url = 'https://github.com/Ch00k/mailhole',
    license = 'LICENSE.txt',
    long_description = open('README.rst').read(),
    entry_points = {
      'console_scripts': [
          'mailhole = mailhole.mailhole:main'
      ]
    },
    packages = ['mailhole'],
)