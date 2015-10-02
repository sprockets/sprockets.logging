Version History
===============

`1.3.2`_ Oct  2, 2015
---------------------
- Switch to packaging as a package instead of a py_module.

`1.3.1`_ Sep 14, 2015
---------------------
- Fix query_arguments handling in Python 3

`1.3.0`_ Aug 28, 2015
---------------------
- Add the traceback and environment if set

`1.2.1`_ Jun 24, 2015
---------------------
- Fix a potential ``KeyError`` when a HTTP request object is not present.

`1.2.0`_ Jun 23, 2015
---------------------
 - Monkeypatch logging.currentframe
 - Include a logging message if it's there

`1.1.0`_ Jun 18, 2015
---------------------
 - Added :class:`sprockets.logging.JSONRequestFormatter`
 - Added :func:`sprockets.logging.tornado_log_function`
 - Added convenience constants and methods as a pass through to Python's logging package:

  - :data:`sprockets.logging.DEBUG` to :data:`logging.DEBUG`
  - :data:`sprockets.logging.ERROR` to :data:`logging.ERROR`
  - :data:`sprockets.logging.INFO` to :data:`logging.INFO`
  - :data:`sprockets.logging.WARN` to :data:`logging.WARN`
  - :data:`sprockets.logging.WARNING` to :data:`logging.WARNING`
  - :func:`sprockets.logging.dictConfig` to :func:`logging.config.dictConfig`
  - :func:`sprockets.logging.getLogger` to :func:`logging.getLogger`

`1.0.0`_ Jun 09, 2015
---------------------
 - Added :class:`sprockets.logging.ContextFilter`

.. _1.3.2: https://github.com/sprockets/sprockets.logging/compare/1.3.1...1.3.2
.. _1.3.1: https://github.com/sprockets/sprockets.logging/compare/1.3.0...1.3.1
.. _1.3.0: https://github.com/sprockets/sprockets.logging/compare/1.2.1...1.3.0
.. _1.2.1: https://github.com/sprockets/sprockets.logging/compare/1.2.0...1.2.1
.. _1.2.0: https://github.com/sprockets/sprockets.logging/compare/1.1.0...1.2.0
.. _1.1.0: https://github.com/sprockets/sprockets.logging/compare/1.0.0...1.1.0
.. _1.0.0: https://github.com/sprockets/sprockets.logging/compare/0.0.0...1.0.0
