"""Freelance - a programm for managing clients, projects and their offers + invoices."""

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = 'Freelance',
    version = '1.0',
    author = 'Manuel Senfft',
    author_email = 'info@tagirijus.de',
    description = ('A client and project management suite.'),
    license = 'BSD',
    keywords = 'self-employed freelancer offer invoice project management',
    url = 'https://github.com/Tagirijus/freelance',
    packages=['freelance'],
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Office/Business',
        'License :: OSI Approved :: BSD License',
    ],
)