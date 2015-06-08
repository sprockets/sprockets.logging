import logging.config
import signal
import uuid

from tornado import ioloop, web
import sprockets.logging


LOG_CONFIG = {
   'version': 1,
   'handlers': {
      'console': {
         'class': 'logging.StreamHandler',
         'stream': 'ext://sys.stdout',
         'formatter': 'simple',
         'filters': ['context'],
      },
   },
   'formatters': {
      'simple': {
         'class': 'logging.Formatter',
         'format': '%(levelname)s %(name)s: %(message)s [%(context)s]',
      },
   },
   'filters': {
      'context': {
         '()': 'sprockets.logging.ContextFilter',
         'properties': ['context'],
      },
   },
   'loggers': {
      'tornado': {
         'level': 'DEBUG',
      },
   },
   'root': {
      'handlers': ['console'],
      'level': 'DEBUG',
   },
   'incremental': False,
}


class RequestHandler(web.RequestHandler):

   def __init__(self, *args, **kwargs):
      self.parent_log = kwargs.pop('parent_log')
      super(RequestHandler, self).__init__(*args, **kwargs)

   def prepare(self):
      uniq_id = self.request.headers.get('X-UniqID', uuid.uuid4().hex)
      self.logger = logging.LoggerAdapter(
         self.parent_log.getChild('RequestHandler'),
         extra={'context': uniq_id})

   def get(self, object_id):
      self.logger.debug('fetchin %s', object_id)
      self.set_status(200)
      return self.finish()

def sig_handler(signo, frame):
   logging.info('caught signal %d, stopping IO loop', signo)
   iol = ioloop.IOLoop.instance()
   iol.add_callback_from_signal(iol.stop)

if __name__ == '__main__':
   logging.config.dictConfig(LOG_CONFIG)
   logger = logging.getLogger('app')
   app = web.Application([
      web.url('/(?P<object_id>\w+)', RequestHandler,
              kwargs={'parent_log': logger}),
   ])
   app.listen(8000)
   signal.signal(signal.SIGINT, sig_handler)
   signal.signal(signal.SIGTERM, sig_handler)
   ioloop.IOLoop.instance().start()
   logger.info('IO loop stopped, exiting')
