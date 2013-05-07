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
    'BaseCommand',
    'BaseShowCommand',
    'BaseListCommand'
]

from cliff.command import Command
from cliff.show import ShowOne
from cliff.lister import Lister


class HelpCommand(Command):
    """
     Print detailed help for another command.
    """

    def get_parser(self, prog_name):
        parser = super(HelpCommand, self).get_parser(prog_name)
        parser.add_argument('cmd',
                            nargs='*',
                            help='name of the command',
                            )
        return parser

    def _get_app_fuzzy_matches(self, app):
        fuzzy_matches = [k for k in self.app.command_manager.commands.keys()
                         if k.startswith(app)]

        return fuzzy_matches

    def _get_sub_command_fuzzy_matches(self, app, sub_command=None):
        sub_commands = self.app.command_manager.commands.get(app, {}).keys()

        # No sub_command specific, return all of the available sub commands
        if not sub_command:
            return sub_commands

        fuzzy_matches = [k for k in sub_commands
                         if k.startswith(sub_command)]

        return fuzzy_matches

    def take_action(self, parsed_args):
        if not parsed_args.cmd:
            cmd_parser = self.get_parser(' '.join([self.app.NAME, 'help']))
            cmd_parser.print_help(self.app.stdout)
            return

        try:
            the_cmd = self.app.command_manager.find_command(
                parsed_args.cmd, called_by_help=True)
            cmd_factory, cmd_name, search_args = the_cmd
        except ValueError:
            exact_match = False
        else:
            exact_match = True

        if exact_match:
            cmd = cmd_factory(self.app, search_args)
            full_name = (cmd_name
                         if self.app.interactive_mode
                         else ' '.join([self.app.NAME, cmd_name])
                         )
            cmd_parser = cmd.get_parser(full_name)
            cmd_parser.print_help(self.app.stdout)
            return

        # Did not find an exact match
        cmd = parsed_args.cmd
        cmd_string = ' '.join(parsed_args.cmd)

        binary = self.app.command_manager.namespace
        app = cmd[0]
        sub_command = None

        if len(cmd) >= 2:
            sub_command = cmd[1]

        app_matches = self._get_app_fuzzy_matches(app=app)

        if not app_matches:
            raise

        self.app.stdout.write('Command "%s" matches:\n\n' % (cmd_string))

        for app_match in app_matches:
            manager_commands = self.app.command_manager.commands[app_match]
            sub_command_matches = \
                self._get_sub_command_fuzzy_matches(app_match, sub_command)

            for sub_command_match in sub_command_matches:
                commands = manager_commands[sub_command_match].keys()

                for command in commands:
                    args = (binary, app_match, sub_command_match, command)
                    self.app.stdout.write(' - %s %s %s %s\n' % args)


class BaseCommand(Command):
    def get_parser(self, prog_name):
        parser = super(BaseCommand, self).get_parser(prog_name=prog_name)
        parser.add_argument('--username', dest='username')
        parser.add_argument('--api-key', dest='api_key')
        parser.add_argument('--api-url', dest='api_url')
        return parser


class BaseShowCommand(BaseCommand, ShowOne):
    def get_parser(self, prog_name):
        parser = super(BaseShowCommand, self).get_parser(prog_name=prog_name)
        parser.add_argument('--id', dest='object_id', required=True)
        return parser


class BaseListCommand(BaseCommand, Lister):
    def get_parser(self, prog_name):
        parser = super(BaseListCommand, self).get_parser(prog_name=prog_name)
        return parser

    @property
    def formatter_default(self):
        return 'paginated_table'
