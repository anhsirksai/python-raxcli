#!/usr/bin/env python
# Copyright 2013 Rackspace
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

from distutils.core import Command
from setuptools import setup, find_packages
from subprocess import call

try:
    long_description = open('README.md', 'rt').read()
except IOError:
    long_description = ''


def read_version_string():
    version = None
    sys.path.insert(0, os.path.join(os.getcwd()))
    from raxcli import __version__
    version = __version__
    sys.path.pop(0)
    return version

# Commands based on Libcloud setup.py:
# https://github.com/apache/libcloud/blob/trunk/setup.py


class Flake8Command(Command):
    description = 'Run flake8 script'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            import flake8
            flake8
        except ImportError:
            print ('Missing "flake8" library. You can install it using pip: '
                   'pip install flake8')
            sys.exit(1)

        cwd = os.getcwd()
        retcode = call(('flake8 %s/raxcli/' % (cwd)).split(' '))
        sys.exit(retcode)


setup(
    name='raxcli',
    version=read_version_string(),
    description='Command line client for the Rackspace Open Cloud',
    long_description=long_description,
    author='Rackspace Hosting',
    author_email='justin.gallardo@rackspace.com',
    url='https://github.com/racker/raxcli',
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: Implementation :: PyPy',
                 'Environment :: Console',
                 ],
    cmdclass={
        'flake8': Flake8Command,
    },
    platforms=['Any'],
    install_requires=[
        # newer version is broken in 2.6, see
        # https://bitbucket.org/catherinedevlin/cmd2/issue/3/fix-a-failure-under-python-26
        #'cmd2 == 0.6.4',
        'cliff == 1.3.1',
        'cliff-tablib >= 1.0',
        'cliff-rackspace >= 0.1.1',
    ],
    dependency_links=[
        'https://github.com/Kami/cliff/tarball/dev#egg=cliff-1.2.2-dev'
    ],
    packages=find_packages(),
    package_dir={
        'raxcli': 'raxcli'
    },
    entry_points={
        'console_scripts': [
            'raxcli = raxcli.main:main'
        ],
        'cliff.formatter.list': [
            'paginated_table = cliff_rackspace.formatters:PaginatedListFormatter',
        ],
    }
)
