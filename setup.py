import os, sys

# Downloads setuptools if not find it before try to import
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup
from fossil import get_version

setup(
    name = 'django-fossil',
    version = get_version(),
    description = "Fossil is a library to store fossilized tracks of objects from Django's ORM",
    author = 'OpenTrials team (Marinho Brandao, Luciano Ramalho and Rafael)',
    author_email = 'opentrials-dev@listas.bireme.br',
    url = 'http://reddes.bvsalud.org/projects/clinical-trials/browser/sandbox/django-fossil',
    license = 'GNU Lesser General Public License (LGPL)',
    packages = ['fossil'],
)

