#!/usr/bin/env python
import re
from setuptools import setup

_version_re = re.compile(r"version\s=\s'(.*)'")


with open('loginpass/_consts.py', 'r') as f:
    version = _version_re.search(f.read()).group(1)


with open('README.rst') as read_me:
    long_description = read_me.read()


setup(
    name='loginpass',
    version=version,
    description='Social connections powered by Authlib for Flask and Django',
    long_description=long_description,
    url='https://authlib.org/',
    zip_safe=False,
    license='BSD',
    packages=['loginpass'],
    install_requires=['Authlib>=0.11'],
    include_package_data=True,
    tests_require=['nose', 'mock'],
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
