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
    'BaseRegistryCommand',
    'BaseRegistryShowCommand',
    'BaseRegistryListCommand',

    'get_client',

    'format_metadata',
    'format_timestamp',
    'format_event_payload'
]

from datetime import datetime

from service_registry.client import Client

from raxcli.config import get_config as get_base_config
from raxcli.commands import BaseCommand, BaseShowCommand, BaseListCommand
from raxcli.apps.registry.constants import SERVICE_EVENTS


class BaseRegistryCommand(BaseCommand):
    def get_parser(self, prog_name):
        parser = super(BaseRegistryCommand, self) \
            .get_parser(prog_name=prog_name)
        parser.add_argument('--region', dest='region')
        return parser


class BaseRegistryShowCommand(BaseRegistryCommand, BaseShowCommand):
    pass


class BaseRegistryListCommand(BaseRegistryCommand, BaseListCommand):
    def get_parser(self, prog_name):
        parser = super(BaseRegistryListCommand, self) \
            .get_parser(prog_name=prog_name)
        parser.add_argument('--limit', dest='limit')
        parser.add_argument('--marker', dest='marker')
        return parser


def get_config():
    return get_base_config(app='registry')


def get_client(parsed_args):
    config = get_config()

    username = config['username']
    api_key = config['api_key']

    if parsed_args.username:
        username = parsed_args.username

    if parsed_args.api_key:
        api_key = parsed_args.api_key

    api_url = parsed_args.api_url
    region = parsed_args.region

    if not username:
        raise ValueError('Missing required argument: username')

    if not api_key:
        raise ValueError('Missing required argument: api-key')

    kwargs = {}

    if api_url is not None:
        kwargs['base_url'] = api_url

    if region is not None:
        kwargs['region'] = region

    c = Client(username=username, api_key=api_key, **kwargs)
    return c


def format_metadata(metadata_dict):
    metadata_str = ''

    count = len(metadata_dict)
    i = 0
    for key, value in metadata_dict.items():
        i += 1
        metadata_str += '%s: %s' % (key, value)

        if i < count:
            metadata_str += ', '

    return metadata_str


def format_timestamp(timestamp):
    if not timestamp:
        return ''

    return datetime.fromtimestamp(timestamp / 1000) \
                   .strftime('%Y-%m-%d %H:%M:%S')


def format_event_payload(event_response):
    event_payload_str = ''
    event_type = event_response['type']
    event_payload = event_response['payload']

    if not event_payload:
        return event_payload_str

    if event_type in SERVICE_EVENTS:
        for key, value in event_payload.iteritems():
            if key == 'metadata':
                metadata_str = format_metadata(value)
                event_payload_str += 'metadata: %s\n' % (metadata_str)
            elif key == 'tags':
                event_payload_str += '%s: %s\n' % (key, ', '.join(value))
            else:
                event_payload_str += '%s: %s\n' % (key, value)
    else:
        for key, value in event_payload.iteritems():
            event_payload_str += '%s: %s\n' % (key, value)
        event_payload_str = event_payload_str.strip(',\n')

    return event_payload_str
