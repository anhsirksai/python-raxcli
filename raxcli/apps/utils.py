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
    'for_all_regions'
]


def for_all_regions(get_client_func, catalog_entry, action_func, parsed_args):
    """
    Run the provided function on all the available regions.

    Available regions are determined based on the user service catalog entries.
    """
    result = []

    # TODO: reuse auth instance
    client = get_client_func(parsed_args)
    catalog = client.connection.get_service_catalog()
    urls = catalog.get_public_urls(service_type=catalog_entry,
                                   name=catalog_entry)

    for api_url in urls:
        parsed_args.api_url = api_url
        client = get_client_func(parsed_args)
        item = action_func(client)
        result.extend(item)

    return result
