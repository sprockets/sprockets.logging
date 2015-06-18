Version History
===============
`1.1.0`_ Jun 18, 2015
---------------------
 - Added :class:`sprockets.logging.JSONRequestFormatter`
 - Added :method:`sprockets.logging.tornado_log_function`
 - Added convenience constants and methods as a pass through to Python's logging package:
  - :data:`sprockets.logging.DEBUG` to :data:`logging.DEBUG`
  - :data:`sprockets.logging.ERROR` to :data:`logging.ERROR`
  - :data:`sprockets.logging.INFO` to :data:`logging.INFO`
  - :data:`sprockets.logging.WARN` to :data:`logging.WARN`
  - :data:`sprockets.logging.WARNING` to :data:`logging.WARNING`
  - :method:`sprockets.logging.dictConfig` to :method:`logging.config.dictConfig`
  - :method:`sprockets.logging.getLogger` to :method:`logging.getLogger`

`1.0.0`_ Jun 09, 2015
---------------------
 - Added :class:`sprockets.logging.ContextFilter`

.. _1.1.0: https://github.com/sprockets/sprockets.logging/compare/1.0.0...1.1.0
.. _1.0.0: https://github.com/sprockets/sprockets.logging/compare/0.0.0...1.0.0
