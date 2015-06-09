"""
Make good log output easier.

- :class:`ContextFilter` adds fixed properties to a log record

"""
from __future__ import absolute_import

import logging


version_info = (1, 0, 0)
__version__ = '.'.join(str(v) for v in version_info)


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
