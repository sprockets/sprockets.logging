sprockets.logging
=================
Making logs nicer since 2015!

|Version| |Downloads| |Status| |Coverage| |License|

Installation
------------
``sprockets.logging`` is available on the
`Python Package Index <https://pypi.python.org/pypi/sprockets.logging>`_
and can be installed via ``pip`` or ``easy_install``:

.. code-block:: bash

   pip install sprockets.logging

Documentation
-------------
https://sprocketslogging.readthedocs.org

Requirements
------------
-  No external requirements

Example
-------
This examples demonstrates how to use ``sprockets.logging`` by ...

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

Source
------
``sprockets.logging`` source is available on Github at `https://github.com/sprockets/sprockets.logging <https://github.com/sprockets/sprockets.logging>`_

License
-------
``sprockets.logging`` is released under the `3-Clause BSD license <https://github.com/sprockets/sprockets.logging/blob/master/LICENSE>`_.


.. |Version| image:: https://badge.fury.io/py/sprockets.logging.svg?
   :target: http://badge.fury.io/py/sprockets.logging

.. |Status| image:: https://travis-ci.org/sprockets/sprockets.logging.svg?branch=master
   :target: https://travis-ci.org/sprockets/sprockets.logging

.. |Coverage| image:: http://codecov.io/github/sprockets/sprockets.logging/coverage.svg?branch=master
   :target: https://codecov.io/github/sprockets/sprockets.logging?branch=master

.. |Downloads| image:: https://pypip.in/d/sprockets.logging/badge.svg?
   :target: https://pypi.python.org/pypi/sprockets.logging

.. |License| image:: https://pypip.in/license/sprockets.logging/badge.svg?
   :target: https://sprocketslogging.readthedocs.org
