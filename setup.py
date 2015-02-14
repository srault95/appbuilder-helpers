# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup

setup(
    name='appbuilder-helpers',
    version="0.1.0",
    description='Helpers for Flask-AppBuilder',
    author='Stéphane RAULT',
    author_email='stephane.rault@radicalspam.org',
    url='https://github.com/srault95/appbuilder-helpers', 
    include_package_data=True,
    packages=('appbuilder_helpers',),
    install_requires = [
        'wtforms<2.0',
        'mongoengine',
        'flask-mongoengine',
        'flask-login<0.3.0',
        'Flask-AppBuilder',
        'pytz',
    ],    
    tests_require=[
        'nose',
        'coverage',
    ],
)
