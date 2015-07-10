
import os
import sys
import abc
import inspect
import shlex

import logbook
from logbook.more import ColorizedStderrHandler

from cliff.app import App
from cliff.commandmanager import CommandManager, EntryPointWrapper

from felicity import __version__, settings
from felicity.utils import import_object, pathjoin, expanduser

from felicity.cli.controller import Controller, UIError

registry = {}

class CommandType(abc.ABCMeta):
    """Metaclass for all Command classes in 'felicity.cli.commands'
    
    Command classes of this type will register themselves in the global
    registry. The registry key will be the lowercased name of the class or, in
    the case of submodules, the name of the class prefixed with the module name.
    Eg. 'felicity.cli.commands.Test' -> 'test'
        'felicity.cli.commands.redis.MGet' -> 'redis mget'
    """

    root = 'felicity.cli.commands.'
    def __new__(cls, name, bases, attrs):
        prefix = attrs['__module__'].partition(cls.root)[2].split('.')
        if prefix and prefix[-1] == 'base':
            prefix = prefix[:-1]
        prefix = ' '.join(prefix)
        prefix = prefix and prefix + ' '
        key = prefix + name.lower()
        t = abc.ABCMeta.__new__(cls, name, bases, attrs)
        registry[key] = EntryPointWrapper(name.lower(), t)
        return t

    @classmethod
    def import_module(cls, name=None):
        """Import submodules of cls.root to pickup classes of type CommandType"""
        if not name:
            module = cls.root.rstrip('.')
        else:
            module = cls.root + name
        import_object(module)

class UICommandManager(CommandManager):

    def load_commands(self, namespace):
        """auto-load Command classes by importing named modules"""
        CommandType.import_module('base')
        self.commands.update(registry)

class UI(App):
    NAME = "felicity"
    LOG = logbook.Logger("felicity.cli")


    def __init__(self, *args, **kwargs):
        kwargs.update(dict(
            description='Dynamic Application Configuration.',
            version=__version__,
            command_manager=UICommandManager('felicity.cli'),
            )
        )
        super(UI, self).__init__(*args, **kwargs)
        self._ctl = None

    def build_option_parser(self, *args, **kwargs):
        parser = super(UI, self).build_option_parser(*args, **kwargs)
        parser.add_argument(
            '-s', '--settings',
            action='store',
            default='settings',
            help="dotted path to settings module (optional)",
        )
        return parser

    def initialize_app(self, argv):
        user_settings = self.options.settings
        settings.configure(user_settings)

    @property
    def ctl(self):
        if self._ctl is None:
            self._ctl = Controller()
        return self._ctl

    def run(self, argv):
        handler = ColorizedStderrHandler(bubble=False)
        with handler:
            return super(UI, self).run(argv)

    def interact(self):
        return self.run(['-h'])

