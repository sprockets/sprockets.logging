"""
Make good log output easier.

- :class:`ContextFilter` adds fixed properties to a log record
- :class:`JSONRequestFormatter` formats log records as JSON output
- :method:`tornado_log_function` is for use as the
    :class`tornado.web.Application.log_function` in conjunction with
    :class:`JSONRequestFormatter` to output log lines as JSON.

"""
from __future__ import absolute_import

from logging import config
import json
import logging

try:
    from tornado import log
except ImportError:
    log = None

version_info = (1, 1, 0)
__version__ = '.'.join(str(v) for v in version_info)

# Shortcut methods and constants to avoid needing to import logging directly
dictConfig = config.dictConfig
getLogger = logging.getLogger

DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
WARNING = logging.WARNING
ERROR = logging.ERROR


class ContextFilter(logging.Filter):
    """
    Ensures that properties exist on a LogRecord.

    :param list|None properties: optional list of properties that
        will be added to LogRecord instances if they are missing

    This filter implementation will ensure that a set of properties
    exists on every log record which means that you can always refer
    to custom properties in a format string.  Without this, referring
    to a property that is not explicitly passed in will result in an
    ugly ``KeyError`` exception.

    """

    def __init__(self, name='', properties=None):
        logging.Filter.__init__(self, name)
        self.properties = list(properties) if properties else []

    def filter(self, record):
        for property_name in self.properties:
            if not hasattr(record, property_name):
                setattr(record, property_name, None)
        return True


class JSONRequestFormatter(logging.Formatter):
    """Instead of spitting out a "human readable" log line, this outputs
    the log data as JSON.

    """
    def format(self, record):
        """Return the log data as JSON

        :param record logging.LogRecord: The record to format
        :rtype: str

        """
        return json.dumps({'name': record.name,
                           'module': record.module,
                           'level': logging.getLevelName(record.levelno),
                           'line_number': record.lineno,
                           'process': record.processName,
                           'timestamp': self.formatTime(record),
                           'thread': record.threadName,
                           'file': record.filename,
                           'request': record.args}, sort_keys=True)


def tornado_log_function(handler):
    """Assigned when creating a :py:class:`tornado.web.Application` instance
    by passing the method as the ``log_function`` argument:

    .. code:: python

        app = tornado.web.Application([('/', RequestHandler)],
                                      log_function=tornado_log_function)

    :type handler: :py:class:`tornado.web.RequestHandler`

    """
    status_code = handler.get_status()
    if status_code < 400:
        log_method = log.access_log.info
    elif status_code < 500:
        log_method = log.access_log.warning
    else:
        log_method = log.access_log.error
    correlation_id = (getattr(handler, 'correlation_id', None) or
                      handler.request.headers.get('Correlation-ID', None))
    log_method('', {'correlation_id': correlation_id,
                    'duration': 1000.0 * handler.request.request_time(),
                    'headers': handler.request.headers,
                    'method': handler.request.method,
                    'path': handler.request.path,
                    'protocol': handler.request.protocol,
                    'query_args': handler.request.query_arguments,
                    'remote_ip': handler.request.remote_ip,
                    'status_code': status_code})
