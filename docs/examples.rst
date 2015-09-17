Examples
========

Simple Usage
------------
The following snippet uses :class:`sprockets.logging.ContextFilter`
to insert context information into a message using a
:class:`logging.LoggerAdapter` instance.

.. literalinclude:: ../examples/simple.py

Dictionary-based Configuration
------------------------------
This package begins to shine if you use the dictionary-based logging
configuration offered by :func:`logging.config.dictConfig`.  You can insert
the custom filter and format string into the logging infrastructure and
insert context easily with :class:`logging.LoggerAdapter`.

.. literalinclude:: ../examples/tornado-app.py


Tornado Application JSON Logging
--------------------------------
If you're looking to log Tornado requests as JSON, the
:class:`sprockets.logging.JSONRequestFormatter` class works in conjunction with
the :func:`tornado_log_function` method to output all Tornado log entries as
JSON objects. In the following example, the dictionary-based configuration is
expanded upon to include specify the :class:`sprockets.logging.JSONRequestFormatter`
as the formatter and passes :func:`tornado_log_function` in as the ``log_function``
when creating the Tornado application.

.. literalinclude:: ../examples/tornado-json-logger.py
