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
    'DEFAULT_ENV_PREFIX',
    'DEFAULT_CONFIG_PATH',

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

    if isinstance(value, bool):
        return value

    return not (value.lower() == 'false')


def get_config(app, default_values=None, config_path=DEFAULT_CONFIG_PATH,
               env_prefix=DEFAULT_ENV_PREFIX, env_dict=None):
    """
    Return dictionary with configuration values for a provided app.

    @param  app: Name of the app configuration is being retrieved for.
    @type   app: C{str}

    @param  default_values: Default configuration values.
    @type   default_values: C{dict}

    @param  config_path: Path to the config file.
    @type   config_path: C{str}

    @param  env_prefix: Environment variables prefix.
    @type   env_prefix: C{str}

    @param  env_dict: Dictionary with environment variables. If not provided,
                      os.environ is used.
    @type   env_dict: C{dict}

    @return Configuration values.
    @rtype: C{dict}
    """
    result = {}

    if env_dict is None:
        env_dict = os.environ

    if default_values is None:
        default_values = {}

    keys = [
        ['global', 'username', 'username'],
        ['global', 'api_key', 'api_key'],
        ['global', 'verify_ssl', 'verify_ssl'],
        ['global', 'auth_url', 'auth_url'],
    ]

    env_keys = ['username', 'api_key', 'api_url', 'auth_url', 'verify_ssl']

    for key in env_keys:
        env_key = env_prefix + key
        env_key = env_key.upper()

        if env_key in env_dict:
            result[key] = env_dict[env_key]

    config_path = env_dict.get(env_prefix + 'RAXRC', config_path)

    config = ConfigParser.ConfigParser()
    config.read(config_path)

    for (config_section, config_key, key) in keys:
        if key in result:
            # Already specified as an env variable
            continue

        # global section
        try:
            value = config.get(config_section, config_key)
        except ConfigParser.Error:
            pass
        else:
            result[key] = value

        # app specific section
        try:
            value = config.get(app, config_key)
        except ConfigParser.Error:
            pass
        else:
            result[key] = value

    if 'verify_ssl' in result:
        result['verify_ssl'] = to_bolean(result['verify_ssl'],
                                         default_value=True)

    for key, value in default_values.items():
        if key not in result:
            result[key] = value

    return result
