#!/usr/bin/env python

import sys
from setuptools import setup

try:
    import cairo
except ImportError:
    print ("Some dependencies could not be found. Make sure to install "
           "the Python bindings for Cairo(import cairo).")
    sys.exit(1)

try:
    import pango
except ImportError:
    print ("Some dependencies could not be found. Make sure to install "
           "the Python bindings for Pango(import pango).")
    sys.exit(1)

try:
    import pangocairo
except ImportError:
    print ("Some dependencies could not be found. Make sure to install "
           "the Python bindings for PangoCairo(import pangocairo).")
    sys.exit(1)

setup(name='shaape',
      version='1.1.0',
      description='Shaape - ascii art to image converter',
      long_description=open('README.asciidoc').read(),
      author='Christian Goltz',
      author_email='goltzchristian@googlemail.com',
      package_data={'shaape': ['data']},
      packages=['shaape'],
      scripts=['bin/shaape'],
      license='LICENSE',
      url='http://github.com/christiangoltz/shaape',
      tests_require=['nose'],
      install_requires=[
          'networkx',
          'PyYAML']
     )
