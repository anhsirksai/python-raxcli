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

from raxcli.utils import get_enum_as_tuples


class TestUtils(unittest.TestCase):
    def test_get_enum_as_tuples(self):
        class EnumClass1(object):
            KEY1 = 0
            KEY_TWO_TWO = 1
            SOME_KEY_SOME_SOME = 2

        result1 = get_enum_as_tuples(EnumClass1, False)
        result2 = get_enum_as_tuples(EnumClass1, True)

        expected1 = [
            (0, 'KEY1'),
            (1, 'KEY_TWO_TWO'),
            (2, 'SOME_KEY_SOME_SOME')
        ]

        expected2 = [
            (0, 'Key1'),
            (1, 'Key Two Two'),
            (2, 'Some Key Some Some')
        ]

        self.assertSetEqual(set(result1), set(expected1))
        self.assertSetEqual(set(result2), set(expected2))


if __name__ == '__main__':
    sys.exit(unittest.main())
