import json
import logging
import random
import unittest
import uuid

import mock

import sprockets.logging

LOGGER = logging.getLogger(__name__)


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


class MockRequest(object):

    headers = {'Accept': 'application/msgpack',
               'Correlation-ID': str(uuid.uuid4())}
    method = 'GET'
    path = '/test'
    protocol = 'http'
    remote_ip = '127.0.0.1'
    query_arguments = {'mock': True}

    def __init__(self):
        self.duration = random.randint(10, 200)

    def request_time(self):
        return self.duration


class MockHandler(object):

    def __init__(self, status_code=200):
        self.status_code = status_code
        self.request = MockRequest()

    def get_status(self):
        return self.status_code


class TornadoLogFunctionTestCase(unittest.TestCase):

    @mock.patch('tornado.log.access_log')
    def test_log_function_return_value(self, access_log):
        handler = MockHandler()
        expectation = ('', {'correlation_id':
                            handler.request.headers['Correlation-ID'],
                            'duration': handler.request.duration * 1000.0,
                            'headers': handler.request.headers,
                            'method': handler.request.method,
                            'path': handler.request.path,
                            'protocol': handler.request.protocol,
                            'query_args': handler.request.query_arguments,
                            'remote_ip': handler.request.remote_ip,
                            'status_code': handler.status_code})
        sprockets.logging.tornado_log_function(handler)
        access_log.assertCalledOnceWith(expectation)


class JSONRequestHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = 32768

    def test_log_function_return_value(self):
        class LoggingHandler(logging.Handler):
            def __init__(self, level):
                super(LoggingHandler, self).__init__(level)
                self.formatter = sprockets.logging.JSONRequestFormatter()
                self.records = []
                self.results = []

            def handle(self, value):
                self.records.append(value)
                self.results.append(self.formatter.format(value))

        logging_handler = LoggingHandler(logging.INFO)
        LOGGER.addHandler(logging_handler)

        handler = MockHandler()
        args = {'correlation_id':
                handler.request.headers['Correlation-ID'],
                'duration': handler.request.duration * 1000.0,
                'headers': handler.request.headers,
                'method': handler.request.method,
                'path': handler.request.path,
                'protocol': handler.request.protocol,
                'query_args': handler.request.query_arguments,
                'remote_ip': handler.request.remote_ip,
                'status_code': handler.status_code}

        LOGGER.info('', args)
        result = logging_handler.results.pop(0)
        keys = ['line_number', 'file', 'level', 'module', 'name',
                'process', 'thread', 'timestamp', 'request']
        value = json.loads(result)
        for key in keys:
            self.assertIn(key, value)
