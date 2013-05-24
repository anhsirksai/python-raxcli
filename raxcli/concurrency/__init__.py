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
    'get_pool',
    'run_function',
    'join_pool'
]

import os
import sys

try:
    import gevent
    gevent
    gevent_available = True
except ImportError:
    gevent_available = False


DEFAULT_BACKEND = 'noop'
BACKEND = DEFAULT_BACKEND
USE_GEVENT = os.getenv('RAXCLI_USE_GEVENT')


if USE_GEVENT and gevent_available:
    BACKEND = 'gevent'

module_name = 'raxcli.concurrency.backends.%s_backend' % (BACKEND)
current_module = sys.modules[__name__]
backend_module = __import__(module_name,
                            fromlist=['raxcli.concurrency.backends'])

for key in __all__:
    func = getattr(backend_module, key)
    setattr(current_module, key, func)

backend_initialize = getattr(backend_module, 'initialize')
backend_initialize()
