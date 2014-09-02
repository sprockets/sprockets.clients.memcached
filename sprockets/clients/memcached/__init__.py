"""
Memcache Client API
===================
The memcache client API wraps the :py:class:`memcache.Client` adding
environment variable based configuration.

Example environment variable configuration:

    ``<PREFIX>_MEMCACHED_SERVERS = '10.0.0.1:11211:64,10.0.0.2:11211:64'``

"""
import logging
import os
import pickle

import memcache

version_info = (0, 0, 0)
__version__ = '.'.join(str(v) for v in version_info)

LOGGER = logging.getLogger(__name__)

DEFAULT_SERVER = '127.0.0.1:11211'

from memcache import _DEAD_RETRY
from memcache import _SOCKET_TIMEOUT
from memcache import SERVER_MAX_KEY_LENGTH
from memcache import SERVER_MAX_VALUE_LENGTH


def _get_servers(prefix):
    """Return the list of memcached servers from the environment variable
    value, defaulting to ``DEFAULT_SERVER`` if it is not set.

    If prefix is not set, then the environment variable ``MEMCACHED_SERVERS``
    will be be used. If both ``<PREFIX>_MEMCACHED_SERVERS`` and
    ``MEMCACHED_SERVERS`` are not set, the default server value of
    ``127.0.0.1`` will be returned.

    :param str prefix: The environment variable prefix
    :rtype: list

    """
    key = '%s_MEMCACHED_SERVERS' % prefix if prefix else 'MEMCACHED_SERVERS'
    return os.environ.get(key, DEFAULT_SERVER).split(',')


class Client(memcache.Client):
    """Wraps :py:class:`memcache.Client`, passing in the environment
    variable prefix. If prefix is set, the environment variable key is in the
    format ``<PREFIX>_MEMCACHED_SERVERS``. If the prefix is not set, the list
    will attempt to be retrieved from the ``MEMCACHED_SERVERS``. If neither
    environment variable is set, the default value of ``127.0.0.1:11211`` is
    used.

    The per server format in the comma separated list is:

        ``[HOST]:[PORT]<:WEIGHT>``

    Where host and port are required but weight is optional.

    :param str prefix: The environment variable prefix. Default: ``None``

    :param int debug: Display error messages when a server can't be contacted.
                      Default: ``0``
    :param int pickle_protocol: number to mandate protocol used by (c)Pickle.

    :param pickler: optional override of default Pickler for subclassing
    :type pickler: :py:class:`pickle.Pickler`

    :param unpickler: optional override of default Unpickler for subclassing
    :type unpickler: :py:class:`pickle.Unpickler`

    :param pload: optional persistent_load function to call on pickle loading
    :type pload: :py:meth:`pickle.loads`

    :param str pid: optional persistent_id function to call on pickle storing

    :param int dead_retry: Number of seconds before retrying a blacklisted
                           server. Default: ``30``

    :param int socket_timeout: Timeout in seconds for all calls to a server.
                               Default: ``3``

    :param server_max_key_length: Data that is larger than this will not be
                                  sent to the server.
                                  Default: ``SERVER_MAX_KEY_LENGTH``
    :type server_max_key_length: int

    :param server_max_value_length: Data that is larger than this will not be
                                    sent to the server.
                                    Default: ``SERVER_MAX_VALUE_LENGTH``
    :type server_max_value_length: int

    :param bool cache_cas: If true, cas operations will be cached. WARNING:
                           This cache is not expired internally, if you have
                           a long-running process you will need to expire it
                           manually via :py:meth:`Client.reset_cas`, or the
                           cache can grow unlimited.
                           Default: ``False``

    :param int flush_on_reconnect: Optional flag which prevents a scenario
                                   that can cause stale data to be read. If
                                   there is more than one memcached server
                                   and the connection to one is interrupted,
                                   keys that mapped to that server will get
                                   reassigned to another. If the first server
                                   comes back, those keys will map to it
                                   again. If it still has its data, ``get()``
                                   can read stale data that was overwritten
                                   on another server. This flag is off by
                                   default for backwards compatibility.
                                   Default: ``0``

    :param bool check_keys: If ``True``, the key is checked to ensure it is
                            the correct length and composed of the right
                            characters.
                            Default: ``True``

    """
    def __init__(self,
                 prefix=None,
                 debug=0,
                 pickle_protocol=0,
                 pickler=pickle.Pickler,
                 unpickler=pickle.Unpickler,
                 pload=None,
                 pid=None,
                 server_max_key_length=SERVER_MAX_KEY_LENGTH,
                 server_max_value_length=SERVER_MAX_VALUE_LENGTH,
                 dead_retry=_DEAD_RETRY,
                 socket_timeout=_SOCKET_TIMEOUT,
                 cache_cas=False,
                 flush_on_reconnect=0,
                 check_keys=True):
        servers = _get_servers(prefix.upper() if prefix else '')
        LOGGER.debug('Connecting to %r', servers)
        super(Client, self).__init__(servers,
                                     debug,
                                     pickle_protocol,
                                     pickler,
                                     unpickler,
                                     pload,
                                     pid,
                                     server_max_key_length,
                                     server_max_value_length,
                                     dead_retry,
                                     socket_timeout,
                                     cache_cas,
                                     flush_on_reconnect,
                                     check_keys)
