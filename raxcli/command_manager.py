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
    'AppCommandManager'
]

import os
import logging

from os.path import join as pjoin
from os.path import basename, splitext
from collections import defaultdict

from cliff.commandmanager import EntryPointWrapper

from raxcli.commands import HelpCommand

LOG = logging.getLogger(__name__)


class AppCommandManager(object):
    """
    Custom command manager which supports commands in the following format:
    <main> <app> <command> <sub command>

    For example: registry services list
    """
    def __init__(self, namespace, apps_path):
        self.commands = defaultdict(dict)
        self.namespace = namespace
        self.apps_path = apps_path
        self._load_commands()

    def _load_commands(self):
        for app_directory in os.listdir(self.apps_path):
            app_path = pjoin(self.apps_path, app_directory)
            app_commands_path = pjoin(app_path, 'commands')

            if not os.path.isdir(app_path) or \
               not os.path.isdir(app_commands_path):
                continue

            app = app_directory

            for commands_directory in os.listdir(app_commands_path):
                commands_path = pjoin(app_commands_path, commands_directory)

                if not os.path.isdir(commands_path):
                    continue

                for command_file in os.listdir(commands_path):
                    if not self._is_command_file(command_file):
                        continue

                    name = splitext(basename(command_file))[0]
                    module_path = '%s.%s.%s.commands.%s.%s' % (
                        self.namespace,
                        'apps',
                        app,
                        commands_directory,
                        name)

                    command_class = '%sCommand' % (
                        name.title().replace('-', ''))
                    LOG.debug('Found command %s %s', name, module_path)

                    try:
                        mod = __import__(module_path, fromlist=[command_class])
                    except ImportError, e:
                        LOG.debug('Failed to load module "%s": %s' %
                                  (module_path, str(e)))
                        continue

                    command_module = getattr(mod, command_class, None)

                    if command_module is None:
                        LOG.debug('Module %s doesn\'t export %s class' %
                                  (module_path, command_class))
                        continue

                    wrapper = EntryPointWrapper(name=name,
                                                command_class=command_module)

                    if not app in self.commands:
                        self.commands[app] = defaultdict(dict)

                    self.commands[app][commands_directory][name] = wrapper

    def _is_command_file(self, name):
        return name.endswith('.py') and name != '__init__.py'

    def __iter__(self):
        return iter(self.commands.items())

    def add_command(self, name, command_class):
        if name == 'help':
            # Overwrite HelpCommand with one which supports commands in the
            # <command> <sub command> class
            command_class = HelpCommand

        self.commands[name]['index'] = EntryPointWrapper(name, command_class)

    def find_command(self, argv, called_by_help=False):
        command = argv[0]
        sub_command = None

        if command == 'help':
            command_entry = self.commands.get('help', {}).get('index', None)
            cmd_factory = command_entry.load()
            args = argv[1:]
            return (cmd_factory, command, args)

        if len(argv) >= 2:
            app = argv[0]
            sub_command = argv[1]
        else:
            app = None

        if len(argv) > 2:
            command = argv[2]
            start_index = 3
        else:
            app = argv[0]
            command = None

        if not command:
            if called_by_help:
                cmd_string = ' '.join(argv).strip()
                raise ValueError('Unknown command: %s' % (cmd_string))

            command_entry = self.commands.get('help', {}).get('index', None)
            cmd_factory = command_entry.load()

            if app:
                args = [app]
            else:
                args = []

            if sub_command:
                args += [sub_command]

            if command:
                args += [command]

            command = ''
            return (cmd_factory, command, args)

        command_entry = self.commands.get(app, {}).get(sub_command, {}) \
            .get(command, None)

        if not command_entry:
            if called_by_help:
                cmd_string = ' '.join(argv).strip()
                raise ValueError('Unknown command: %s' % (cmd_string))
            else:
                command_entry = self.commands.get('help', {}) \
                                             .get('index', None)
                cmd_factory = command_entry.load()

                if app:
                    args = [app]
                else:
                    args = []

                if sub_command:
                    args += [sub_command]

                args += [command]

                return (cmd_factory, command, args)

        cmd_factory = command_entry.load()
        args = argv[start_index:]
        command_name = '%s %s' % (command, sub_command)
        return (cmd_factory, command_name, args)
