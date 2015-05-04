# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
import shutil

try:
    from io import BytesIO
except ImportError:
    from cStringIO import StringIO as BytesIO

import logbook

log = logbook.Logger(__name__)


class UIError(Exception):
    pass

class PathExists(UIError):
    
    def __str__(self):
        return "path exists '%s'" % self.args[0]

class PathDoesNotExist(UIError):
    
    def __str__(self):
        return "invalid path '%s'" % self.args[0]

def mkdir(path):
    if pathexists(path):
        return
    try:
        os.makedirs(path)
    except:
        raise UIError("couldn't create directory '%s'" % path)

class Writer(object):

    def __init__(self, stream=None, encoding='utf-8'):
        self.stream = stream or BytesIO()

    def write(self, text=''):
        self.stream.write(text.encode(self.encoding))
        self.stream.write('\n')

class Controller(object):
    pass

