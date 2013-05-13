#!/usr/bin/env python

from distutils.core import setup

setup(name='shaape',
      version='1.0.0',
      description='Shaape - ascii art to image converter',
      author='Christian Goltz',
      author_email='goltzchristian@googlemail.com',
      package_data = {'shaape':['data']},
      packages=['shaape'],
      scripts=['bin/shaape'],
      license='LICENSE',
      url='http://github.com/christiangoltz/shaape',
      requires=[
          'networkx',
          'cairo',
          'yaml',
          'pango',
          'pangocairo']
     )
