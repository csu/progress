#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
  name='makeprogress',
  version='0.0.3.2',
  description='Use progress to manage weekly snippets.',
  long_description=open('README').read(),
  author='Christopher Su',
  author_email='gh@christopher.su',
  url='https://github.com/csu/progress',
  packages=find_packages(),
  package_data={
    'progress': ['static/*', 'templates/*']
  },
  install_requires=[
    'Flask==0.10.1',
    'itsdangerous==0.24',
    'Jinja2==2.8',
    'MarkupSafe==0.23',
    'pyandoc==0.0.1',
    'sh==1.11',
    'Werkzeug==0.11.3',
    'wheel==0.24.0',
  ],
  entry_points={
    'console_scripts': [
      'progress=progress.server:main'
    ],
  }
)
