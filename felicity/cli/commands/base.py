
import os
import sys
import argparse

import six
import logbook
import pytest
from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne

from felicity import settings
from felicity.cli.controller import UIError
from felicity.cli.application import CommandType
from felicity.utils import pathjoin, pathexists

log = logbook.Logger("felicity.cli")

@six.add_metaclass(CommandType)
class Test(Command):
    """Run non-django tests"""

    def get_parser(self, *args, **kwargs):
        parser = super(Test, self).get_parser(*args, **kwargs)
        parser.add_argument(
            'target',
            help="the directory or python module to test",
        )
        return parser

    def take_action(self, args):
        cmdline = "-vv --cov felicity --cov-report term".split()
        cmdline.append(args.target)
        assert settings.configured
        pytest.main(cmdline)

