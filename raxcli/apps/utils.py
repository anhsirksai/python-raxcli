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
from os.path import join as pjoin, expanduser

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

CREDENTIALS_FILE = '.raxrc'
CONFIG_PATH = pjoin(expanduser('~'), CREDENTIALS_FILE)


def get_config():
    keys = [['credentials', 'username', 'username'],
            ['credentials', 'api_key', 'api_key'],
            ['api', 'url', 'api_url'],
            ['auth_api', 'url', 'auth_url'],
            ['ssl', 'verify', 'ssl_verify']]

    result = {}

    result['username'] = os.getenv('RAX_USERNAME', None)
    result['api_key'] = os.getenv('RAX_API_KEY', None)
    result['api_url'] = os.getenv('RAX_API_URL', None)
    result['auth_url'] = os.getenv('RAX_AUTH_URL', None)
    result['ssl_verify'] = os.getenv('RAX_SSL_VERIFY', None)

    config = ConfigParser.ConfigParser()
    config.read(os.getenv('RAX_RAXRC') or CONFIG_PATH)

    for (config_section, config_key, key) in keys:
        if result[key]:
            # Already specified as an env variable
            continue

        try:
            value = config.get(config_section, config_key)
        except ConfigParser.Error:
            continue

        result[key] = value

    # convert "false" to False
    if result['ssl_verify']:
        result['ssl_verify'] = not (result['ssl_verify'].lower() == 'false')
    else:
        result['ssl_verify'] = True

    return result
