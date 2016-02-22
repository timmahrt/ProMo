'''
Created on Aug 29, 2014

@author: tmahrt
'''
from distutils.core import setup
setup(name='prosodyMorph',
      version='1.1.0',
      author='Tim Mahrt',
      author_email='timmahrt@gmail.com',
      package_dir={'promo':'promo'},
      packages=['promo',
                'promo.morph_utils'],
      license='LICENSE',
      long_description=open('README.rst', 'r').read(),
#       install_requires=[], # No requirements! # requires 'from setuptools import setup'
      )