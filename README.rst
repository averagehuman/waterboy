Felicity - Dynamic Application settings
=======================================

A library for storing editable settings in pluggable backend data stores.

The idea is that a given application will have a configuration context
consisting of both those settings which are not expected to vary for any given
deployment, and those settings which may vary during the lifetime of a
deployment (for example, third party keys or urls). It is these latter settings
which we want to store in some backend data store in order to make them more
easily editable by an application user or administrator.

This is a forked and significantly updated version of `django-constance`_.

`felicity`_ aims to be framework-agnostic but will fall back to use Django
settings if possible, and in this case will work similarly to the original
project.

`felicity`_ currently has builtin support for Redis, MongoDB and Django model
backends.

Settings and Config
-------------------

The different settings types are represented in `felicity`_ by a
*Settings* class and a *Config* class. It is for a settings object (most
likely populated via some python module) to define a *CONFIG* attribute which
is of the form::

    CONFIG = {
        '<KEY>': (<DEFAULT>, '<HELP TEXT>'),
        ...
    }

For example::

    CONFIG = {
        'INT_VALUE': (1, 'some int'),
        'LONG_VALUE': (long_value, 'some looong int'),
        'BOOL_VALUE': (True, 'true or false'),
        'STRING_VALUE': ('Hello world', 'greetings'),
        'UNICODE_VALUE': (six.u('Rivière-Bonjour'), 'greetings'),
        'DECIMAL_VALUE': (Decimal('0.1'), 'the first release version'),
        'DATETIME_VALUE': (datetime(2010, 8, 23, 11, 29, 24),
                           'time of the first commit'),
        'FLOAT_VALUE': (3.1415926536, 'PI'),
        'DATE_VALUE': (date(2010, 12, 24), 'Merry Chrismas'),
        'TIME_VALUE': (time(23, 59, 59), 'And happy New Year'),
    }

Attempts to get or set values on the *Config* object will fail with a KeyError
if the key does not exist in the *CONFIG* setting.

.. _django-constance: http://django-constance.readthedocs.org/
.. _felicity: https://github.com/gmflanagan/felicity

