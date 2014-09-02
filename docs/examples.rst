Examples
========
The following example sets the environment variables for connecting to
memcached on ``192.168.1.2`` and ``192.168.1.3`` and subsequently issuing a few
memcached commands:

.. code:: python

    import os

    from sprockets.clients import memcached

    os.environ['MEMCACHED_SERVERS'] = '192.168.1.2:11211,192.168.1.3:11211'

    client = memcached.Client()
    client.set('foo', 'bar')
    print(client.get('foo'))

The next example uses a prefixed environment variable for configuration data:

.. code:: python

    import os

    from sprockets.clients import memcached

    os.environ['FOO_MEMCACHED_SERVERS'] = '192.168.1.2:11211'

    client = memcached.Client('foo')
    client.set('foo', 'bar')
    print(client.get('foo'))
