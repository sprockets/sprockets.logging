import logging
import sys

import sprockets.logging


formatter = logging.Formatter('%(levelname)s %(message)s {%(context)s}')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
handler.addFilter(sprockets.logging.ContextFilter(properties=['context']))
logging.Logger.root.addHandler(handler)
logging.Logger.root.setLevel(logging.DEBUG)

# Outputs: INFO Hi there {None}
logging.info('Hi there')

# Outputs: INFO No KeyError {bah}
logging.info('No KeyError', extra={'context': 'bah'})

# Outputs: INFO Now with context! {foo}
adapted = logging.LoggerAdapter(logging.Logger.root, extra={'context': 'foo'})
adapted.info('Now with context!')
