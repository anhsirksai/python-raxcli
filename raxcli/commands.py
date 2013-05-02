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

__all__ = [
    'BaseCommand',
    'BaseShowCommand',
    'BaseListCommand'
]

from cliff.command import Command
from cliff.show import ShowOne
from cliff.lister import Lister


class BaseCommand(Command):
    def get_parser(self, prog_name):
        parser = super(BaseCommand, self).get_parser(prog_name=prog_name)
        parser.add_argument('--username', dest='username')
        parser.add_argument('--api-key', dest='api_key')
        parser.add_argument('--api-url', dest='api_url')
        return parser


class BaseShowCommand(BaseCommand, ShowOne):
    def get_parser(self, prog_name):
        parser = super(BaseShowCommand, self).get_parser(prog_name=prog_name)
        parser.add_argument('--id', dest='object_id', required=True)
        return parser


class BaseListCommand(BaseCommand, Lister):
    def get_parser(self, prog_name):
        parser = super(BaseListCommand, self).get_parser(prog_name=prog_name)
        return parser

    @property
    def formatter_default(self):
        return 'paginated_table'
