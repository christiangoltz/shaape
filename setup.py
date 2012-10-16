#!/usr/bin/env python

from distutils.core import setup

setup(name='shaape',
      version='0.1.1',
      description='Shaape - Ascii art to image converter',
      author='Christian Goltz',
      author_email='goltzchristian@googlemail.com',
      package_dir = {'shaape':'src'},
      package_data = {'shaape':['data']},
      packages=['shaape'],
      url='http://github.com/christiangoltz/shaape',
      requires=['networkx','cairo']
     )
