Examples
========

Simple Usage
------------
The following snippet uses :class:`sprockets.logging.filters.ContextFilter`
to insert context information into a message using a
:class:`logging.LoggerAdapter` instance.

.. code-block:: python

   import logging
   import sys

   import sprockets.logging

   formatter = logging.Formatter('%(levelname)s %(message)s {%(context)s}')
   handler = logging.StreamHandler(sys.stdout)
   handler.setFormatter(formatter)
   handler.addFilter(sprockets.logging.ContextFilter(properties=['context']))
   logging.Logger.root.addHandler(handler)

   # Outputs: INFO Hi there {}
   logging.info('Hi there')

   # Outputs: INFO No KeyError {bah}
   logging.info('No KeyError', extra={'context': 'bah'})

   # Outputs: INFO Now with context! {foo}
   adapted = logging.LoggerAdapter(logging.Logger.root, extra={'context': 'foo'})
   adapter.info('Now with context!')
