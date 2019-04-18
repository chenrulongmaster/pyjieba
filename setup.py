# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='pyjieba',
    version = '1.0',
    description=('CPPJieba python wrapper'),
    keywords = ('jieba', 'cppjieba', 'pyjieba'),
    license = 'Apache-2.0',
    author = 'chen ru long',
    author_email = 'chenrulong0513.master@gmail.com',
    packages = find_packages(where='.', exclude=['cppjieba_src/**']),
    package_data={'': ['*']},
    include_package_data=True,
    platforms = 'any',
    install_requires = [],
    url='https://github.com/chenrulongmaster/pyjieba',
    long_description=open('README.rst').read()
)
