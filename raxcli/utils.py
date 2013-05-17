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
    'get_enum_as_dict'
]


def get_enum_as_dict(cls, reverse=False, friendly_names=False):
    """
    Convert an "enum" class to a dict key is the enum name and value is an enum
    value.
    """
    result = {}
    for key, value in cls.__dict__.items():
        if key.startswith('__'):
            continue

        if key[0] != key[0].upper():
            continue

        name = key

        if friendly_names:
            name = name.replace('_', ' ').lower().title()

        if reverse:
            result[value] = name
        else:
            result[name] = value

    return result
