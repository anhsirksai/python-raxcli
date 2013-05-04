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

from raxcli.apps.monitoring.utils import (MonitoringEntityListCommand,
                                          get_client)
from raxcli.apps.monitoring.resources import Alarm, Collection, Placeholder


class ListCommand(MonitoringEntityListCommand):
    """
    Return a list of alarms.
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        client = get_client(parsed_args)

        marker = parsed_args.marker if parsed_args.marker else None
        kwargs = {'ex_next_marker': marker}

        entity = Placeholder(parsed_args.entity_id)
        alarms = [Alarm(alarm)
                  for alarm in client.list_alarms(entity,
                                                  **kwargs)]
        collection = Collection(alarms)
        return collection.generate_output()
