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

from cliff.show import ShowOne

from raxcli.apps.servers.utils import BaseServerCommand, get_client
from raxcli.apps.servers.resources import Node


class CreateCommand(BaseServerCommand, ShowOne):
    """
    Create a node
    """
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CreateCommand, self).get_parser(prog_name=prog_name)
        parser.add_argument('--name', dest='name', required=True)
        parser.add_argument('--flavor', dest='flavor', required=True)
        parser.add_argument('--image', dest='image', required=True)
        parser.add_argument('--region', dest='region', required=True,
                            help='(ord, dfw, lon)')
        return parser

    def take_action(self, parsed_args):
        client = get_client(parsed_args)
        images = client.list_images()
        image = [i for i in images if i.id == parsed_args.image]
        if len(image) == 0:
            raise Exception('Invalid Image')
        sizes = client.list_sizes()
        flavor = [s for s in sizes if s.id == parsed_args.flavor][0]
        if len(flavor) == 0:
            raise Exception('Invalid Flavor')
        node = Node(client.create_node(name=parsed_args.name, image=image[0],
                    size=flavor[0]))
        return node.generate_output()
