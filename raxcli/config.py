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
    'get_config'
]

import os
from os.path import join as pjoin, expanduser

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

DEFAULT_CREDENTIALS_FILE = '.raxrc'
DEFAULT_ENV_PREFIX = 'RAXCLI_'

DEFAULT_CONFIG_PATH = pjoin(expanduser('~'), DEFAULT_CREDENTIALS_FILE)


def to_bolean(value, default_value=False):
    """
    Convert string value to a boolean.
    """
    if value is None:
        return default_value

    return not (value.lower() == 'false')


def get_config(app, config_path=DEFAULT_CONFIG_PATH,
               env_prefix=DEFAULT_ENV_PREFIX):
    """
    Return dictionary with configuration values for a provided app.
    """

    keys = [
        ['global', 'username', 'username'],
        ['global', 'api_key', 'api_key'],
        ['global', 'verify_ssl', 'verify_ssl'],
        ['global', 'auth_url', 'auth_url'],
    ]

    result = {}

    result['username'] = os.getenv(env_prefix + 'USERNAME', None)
    result['api_key'] = os.getenv(env_prefix + 'API_KEY', None)
    result['api_url'] = os.getenv(env_prefix + 'API_URL', None)
    result['auth_url'] = os.getenv(env_prefix + 'AUTH_URL', None)
    result['verify_ssl'] = os.getenv(env_prefix + 'SSL_VERIFY', None)

    config_path = os.getenv(env_prefix + 'RAXRC', config_path)

    config = ConfigParser.ConfigParser()
    config.read(config_path)

    for (config_section, config_key, key) in keys:
        if result[key]:
            # Already specified as an env variable
            continue

        # global section
        try:
            value = config.get(config_section, config_key)
        except ConfigParser.Error:
            continue

        result[key] = value

        # app specific section
        try:
            value = config.get(app, config_key)
        except ConfigParser.Error:
            continue

        result[key] = value

    result['verify_ssl'] = to_bolean(result['verify_ssl'], default_value=True)

    return result
