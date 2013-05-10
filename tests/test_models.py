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

import sys
import unittest2 as unittest

from raxcli.models import Attribute, Model, Collection


class Entity(Model):
    id = Attribute(src='key')
    label = Attribute()


class FakeEntity1(object):
    key = 'key1'
    ip = '127.0.0.1'
    label = 'test label'


class FakeEntity2(object):
    key = 'key2'
    ip = '127.0.0.1'
    label = 'label2'


class TestModels(unittest.TestCase):
    def test_generate_output(self):
        en1 = Entity(FakeEntity1())
        en2 = Entity(FakeEntity2())

        collection = Collection([en1, en2])

        result1 = en1.generate_output()
        expected1 = (
            ['id', 'label'],
            ['key1', 'test label']
        )

        result2 = collection.generate_output()
        expected2 = (
            ['id', 'label'],
            [
                ['key1', 'test label'],
                ['key2', 'label2']
            ]
        )

        self.assertSequenceEqual(result1, expected1)
        self.assertSequenceEqual(result2, expected2)


if __name__ == '__main__':
    sys.exit(unittest.main())
