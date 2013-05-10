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

from raxcli.models import Placeholder, Collection
from raxcli.apps.loadbalancer.resources import Member
from raxcli.apps.loadbalancer.utils import get_client
from raxcli.apps.loadbalancer.utils import LoadBalancerBalancerListCommand


class ListMembersCommand(LoadBalancerBalancerListCommand):
    """
    Output a list of the members attached to the provided loadbalancer.
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        client = get_client(parsed_args)
        balancer = Placeholder(parsed_args.balancer_id)

        members = client.balancer_list_members(balancer=balancer)
        members = [Member(m) for m in members]
        collection = Collection(members)
        return collection.generate_output()
