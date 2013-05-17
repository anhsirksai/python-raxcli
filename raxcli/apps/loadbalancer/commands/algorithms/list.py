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

import logging

from libcloud.loadbalancer.base import Algorithm

from raxcli.models import Collection
from raxcli.apps.loadbalancer.resources import Algorithm as AlgorithmModel
from raxcli.commands import BaseListCommand
from raxcli.utils import get_enum_as_dict
from raxcli.apps.loadbalancer.utils import LoadBalancerCommand, get_client


class ListCommand(LoadBalancerCommand, BaseListCommand):
    """
    Output a list of the available loadbalancing algorithms.
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        client = get_client(parsed_args)

        available_algorithms = get_enum_as_dict(Algorithm, True)
        algorithms = client.list_supported_algorithms()

        result = []
        for algorithm, id in available_algorithms.items():
            if id in algorithms:
                result.append(AlgorithmModel({'id': id,
                                              'algorithm': algorithm}))

        collection = Collection(result)
        return collection.generate_output()
