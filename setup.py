# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='statsd_decorators',
    version='0.0.1',
    description='Decorators for python-statsd',
    long_description=readme,
    author='Jeremiah Malina',
    author_email='jmalina327@gmail..com',
    url='https://github.com/jjmalina/statsd-decorators',
    license=license,
    packages=find_packages(exclude=('tests',))
)

