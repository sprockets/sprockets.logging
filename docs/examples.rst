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
