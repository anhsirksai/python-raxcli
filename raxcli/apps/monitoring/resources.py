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

import copy
from inspect import getmembers


class Placeholder(object):
    """
    Some libcloud calls require an object with the id field instead of
    just taking an id.
    """
    def __init__(self, id):
        self.id = id


class Attribute(object):
    """
    Generic attribute that represents a field on a resource.
    """
    def __init__(self, view_single=True, view_list=True):
        self.view_single = view_single
        self.view_list = view_list


class Object(object):
    """
    Generic object that allows you to declaratively define how resources
    should be presented.
    """
    def get_attrs(self, view_type=None):
        attrs = []
        for attr, _ in getmembers(self):
            field = getattr(self, attr)
            if not isinstance(field, Attribute):
                continue
            if not view_type or getattr(field, view_type):
                attrs.append(attr)
        return attrs

    def __init__(self, obj):
        for attr in self.get_attrs():
            field = getattr(self, attr)
            field.value = getattr(obj, attr)
            setattr(self, attr, copy.copy(field))

    def generate_output(self):
        columns = self.get_fields(view_type='view_single')
        data = [getattr(self, attr).value for attr in columns]
        return (columns, data)


class Collection(object):
    """
    A collection of resources for outputting to a list.
    """
    def __init__(self, objs):
        self.objs = objs

    def generate_output(self):
        columns = []
        data = []
        for obj in self.objs:
            if not columns:
                columns = obj.get_fields(view_type='view_list')
            data.append([getattr(obj, attr).value for attr in columns])
        return (columns, data)


class Check(Object):
    """
    Check resource.
    """
    id = Attribute()
    label = Attribute()
    type = Attribute()
    entity_id = Attribute(view_list=False)
    monitoring_zones = Attribute(view_list=False)
    period = Attribute(view_list=False)
    timeout = Attribute(view_list=False)
    target_alias = Attribute(view_list=False)
    target_resolver = Attribute(view_list=False)
    disabled = Attribute(view_list=False)
    details = Attribute(view_list=False)
