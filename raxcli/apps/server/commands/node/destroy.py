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

from raxcli.apps.server.utils import BaseServerCommand, get_client
from raxcli.apps.server.resources import Node
from raxcli.models import Collection


class DestroyCommand(BaseServerCommand):
    """
    Destroy a node
    """
    log = logging.getLogger(__name__)


    def get_parser(self, prog_name):
        parser = super(DestroyCommand, self).get_parser(prog_name=prog_name)
        parser.add_argument('--id', dest='id', required=True)
        parser.add_argument('--region', dest='region', required=True,
            help='(ord, dfw, lon)')
        return parser


    def take_action(self, parsed_args):
        client = get_client(parsed_args)
        nodes = client.list_nodes()
        node = [n for n in nodes if n.id == parsed_args.id][0]
        client.destroy_node(node)