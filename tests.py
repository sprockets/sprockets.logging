import logging
import uuid
import unittest

import sprockets.logging


class Prototype(object):
    pass


class RecordingHandler(logging.FileHandler):
    def __init__(self):
        logging.FileHandler.__init__(self, filename='/dev/null')
        self.log_lines = []

    def format(self, record):
        log_line = logging.FileHandler.format(self, record)
        self.log_lines.append(log_line)
        return log_line


class ContextFilterTests(unittest.TestCase):

    def setUp(self):
        super(ContextFilterTests, self).setUp()
        self.logger = logging.getLogger(uuid.uuid4().hex)
        self.handler = RecordingHandler()
        self.logger.addHandler(self.handler)

    def test_that_filter_blocks_key_errors(self):
        formatter = logging.Formatter('%(message)s [%(context)s]')
        self.handler.setFormatter(formatter)
        self.handler.addFilter(sprockets.logging.ContextFilter(
            properties=['context']))
        self.logger.info('hi there')

    def test_that_filter_does_not_overwrite_extras(self):
        formatter = logging.Formatter('%(message)s [%(context)s]')
        self.handler.setFormatter(formatter)
        self.handler.addFilter(sprockets.logging.ContextFilter(
            properties=['context']))
        self.logger.info('hi there', extra={'context': 'foo'})
        self.assertEqual(self.handler.log_lines[-1], 'hi there [foo]')
