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

from raxcli.commands import BaseCommand, BaseListCommand
from raxcli.config import get_config as get_base_config

from libcloud.loadbalancer.providers import get_driver
from libcloud.loadbalancer.types import Provider

import libcloud.security

CA_CERT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            '../data/cacert.pem')
libcloud.security.CA_CERTS_PATH.insert(0, CA_CERT_PATH)


class LoadBalancerCommand(BaseCommand):
    def get_parser(self, prog_name):
        parser = super(LoadBalancerCommand, self).\
            get_parser(prog_name=prog_name)
        parser.add_argument('--auth-url', dest='auth_url')
        parser.add_argument('--region', dest='region')
        return parser


class LoadBalancerBalancerListCommand(LoadBalancerCommand, BaseListCommand):
    def get_parser(self, prog_name):
        parser = super(LoadBalancerBalancerListCommand, self).\
            get_parser(prog_name=prog_name)
        parser.add_argument('--balancer-id', dest='balancer_id', required=True)
        return parser


def get_config():
    return get_base_config(app='loadbalancer')


def for_all_regions_list(parsed_args, func):
    output = []
    # TODO: others, LON?
    lbregions = ['ord', 'dfw']
    for region in lbregions:
        parsed_args.region = region
        client = get_client(parsed_args)
        output.extend(func(client))
    return output


def get_client(parsed_args):
    config = get_config()
    # TODO: regions/uk
    driver = get_driver(Provider.RACKSPACE_US)

    username = config['username']
    api_key = config['api_key']
    if parsed_args.username:
        username = parsed_args.username
    if parsed_args.api_key:
        api_key = parsed_args.api_key

    api_url = parsed_args.api_url
    auth_url = parsed_args.auth_url

    if not username:
        raise ValueError('Missing required argument: username')

    if not api_key:
        raise ValueError('Missing required argument: api-key')

    options = {}

    if api_url is not None:
        options['ex_force_base_url'] = api_url

    if auth_url is not None:
        options['ex_force_auth_url'] = auth_url

    if parsed_args.region is not None:
        options['ex_force_region'] = parsed_args.region

    return driver(username, api_key, **options)
