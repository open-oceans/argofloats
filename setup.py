import sys
import os
import sys
import setuptools
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
from distutils.version import StrictVersion
from setuptools import __version__ as setuptools_version

if StrictVersion(setuptools_version) < StrictVersion('38.3.0'):
    raise SystemExit(
        'Your `setuptools` version is old. '
        'Please upgrade setuptools by running `pip install -U setuptools` '
        'and try again.'
    )


def readme():
    with open('README.md') as f:
        return f.read()
setuptools.setup(
    name='argofloats',
    version='0.0.2',
    packages=['argofloats'],
    url='https://github.com/samapriya/argofloats',
    package_data={'': ['bundles.json']},
    install_requires=['requests>=2.24.0',
                      'area>=1.1.1',
                      'beautifulsoup4>=4.10.0',
                      'geojson>=2.5.0',
                      'tenacity>=8.0.1',
                      'pandas>=1.3.5',
                      'pyproj>=1.9.5.1;platform_system!="Windows"',
                      'shapely>=1.6.4;platform_system!="Windows"',
                      'fiona>=1.8.6;platform_system!="Windows"',
                      'geopandas>=0.5.0;platform_system!="Windows"'
                      ],
    license='Apache 2.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.4',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: GIS',
    ),
    author='Samapriya Roy',
    author_email='samapriya.roy@gmail.com',
    description='Simple CLI for ArgoVis & Argofloats',
    entry_points={
        "console_scripts": ["argofloats=argofloats.argofloats:main"]
    },
)
