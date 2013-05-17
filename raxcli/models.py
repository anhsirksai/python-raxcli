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
    'Placeholder',
    'Model',
    'Attribute',
    'Collection'
]

import copy

from operator import itemgetter
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
    _creation_count = 0

    def __init__(self, src=None, view_single=True, view_list=True):
        """
        @keyword src: Optional name of the field on the object which acts as a
                      source for this attribute.
        @keyword src: C{str}
        """
        self.src = src
        self.view_single = view_single
        self.view_list = view_list

        # Keep a count that is incremented on instantiation so we can iterate
        # in the same order that attributes are delcared on an Object.
        self._creation_count = Attribute._creation_count + 1
        Attribute._creation_count = self._creation_count


class Model(object):
    """
    Generic object that allows you to declaratively define how resources
    should be presented.
    """
    def get_attrs(self, view_type=None):
        """
        Get model attributes for the provided view_type.
        """
        attrs = []
        for attr, _ in getmembers(self):
            field = getattr(self, attr)

            if not isinstance(field, Attribute):
                continue

            if not view_type or getattr(field, view_type):
                src = field.src if field.src else attr
                attrs.append((field._creation_count, [attr, src]))

        return [attr for field, attr in sorted(attrs, key=itemgetter(0))]

    def __init__(self, obj):
        for name, source in self.get_attrs():
            field = getattr(self, name)
            field.value = getattr(obj, source)
            setattr(self, name, copy.copy(field))

    def generate_output(self):
        columns = [attr for attr, _ in self.get_attrs(view_type='view_single')]
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
                columns = [attr for attr, _ in
                           obj.get_attrs(view_type='view_list')]
            data.append([getattr(obj, attr).value for attr in columns])

        return (columns, data)
