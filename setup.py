import os, sys

# Downloads setuptools if not find it before try to import
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup
import fossil

setup(
    name = 'django-fossil',
    version = fossil.__version__,
    description = "Fossil is a library to store fossilized tracks of objects from Django's ORM",
    author = fossil.__author__,
    author_email = 'opentrials-dev@listas.bireme.br',
    url = fossil.__url__,
    license = fossil.__license__,
    packages = ['fossil'],
)

