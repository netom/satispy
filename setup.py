#!/usr/bin/env python
# -*- coding: utf8 -*-

from setuptools import setup

setup(
    name='satispy',
    version='1.0a5',
    description='An interface to SAT solver tools (like minisat)',
    author='FÁBIÁN Tamás László',
    author_email='giganetom@gmail.com',
    url='https://github.com/netom/satispy/',
    download_url='https://github.com/netom/satispy/tarball/1.0a5#egg=satispy-1.0a5',
    license='BSD License',
    platforms='OS Independent',
    packages=['satispy', 'satispy.io', 'satispy.solver'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries'
    ],
)
