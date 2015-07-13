Waterboy - Dynamic Application settings
=======================================

`waterboy`_ is a library that enables the storing of editable application
settings in a backend data store (Redis and MongoDB currently supported).

The idea is that a given application will have a configuration context
consisting of both those settings which are not expected to vary for any given
deployment, and those settings which may vary or which must be accessible from
outside the application (for example, third party keys or urls). It is these
latter "live" settings which we want to store in order to make them more
easily editable by an application user or administrator.

This was originally a fork of `django-constance`_, but is now independent of
Django and is essentially the backend-abstraction part of the original library.

Usage
-----

In your application configuration you define the settings that you want to be
editable in a dictionary of the form::

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

Then create a Config object based on these initial settings. For example, using Redis::

    >>> from waterboy import RedisConfig
    >>> cfg = RedisConfig(initial=CONFIG)

You then retrieve settings from the backend with attribute-style access.

    >>> cfg.INT_VALUE
    1

If the backend returns None then the default value is returned.

Similarly, setting an attribute on the Config object will transparently "upsert"
that value in the backend.

Attempts to get or set values on the Config object will fail with an AttributeError
if the key does not exist in the initial defaults dictionary.

But this behaviour may be modified by passing **strict=False** to the Config constructor::

    >>> cfg = RedisConfig(initial=CONFIG, strict=False)

which will cause the existence check to be bypassed::

    >>> cfg.ABCD = 'abcd'

Development
-----------

The source is on `github`_.

Clone and run tests::

    $ git clone git@codebasehq.com:gflanagan/python/waterboy.git
    $ cd waterboy
    $ make test

Tests are run via tox and pytest.

If redis and mongo are not running on the standard ports then the tests associated
with those backends will be skipped.

To install redis and mongo locally, run buildout::

    $ make buildout

Then run redis in the foreground with::

    $ ./bin/redis-server

.. _django-constance: http://django-constance.readthedocs.org/
.. _waterboy: https://github.com/gmflanagan/waterboy
.. _github: https://github.com/gmflanagan/waterboy

