import json
import logging
import os
import unittest
import uuid

from tornado import web, testing

import sprockets.logging


def setup_module():
    os.environ.setdefault('ENVIRONMENT', 'development')


class SimpleHandler(web.RequestHandler):

    def get(self):
        if self.get_query_argument('runtime_error', default=None):
            raise RuntimeError(self.get_query_argument('runtime_error'))
        if self.get_query_argument('status_code', default=None) is not None:
            self.set_status(int(self.get_query_argument('status_code')))
        else:
            self.set_status(204)


class RecordingHandler(logging.Handler):

    def __init__(self):
        super(RecordingHandler, self).__init__()
        self.emitted = []

    def emit(self, record):
        self.emitted.append((record, self.format(record)))


class TornadoLoggingTestMixin(object):

    def setUp(self):
        super(TornadoLoggingTestMixin, self).setUp()
        self.access_log = logging.getLogger('tornado.access')
        self.app_log = logging.getLogger('tornado.application')
        self.gen_log = logging.getLogger('tornado.general')
        for logger in (self.access_log, self.app_log, self.gen_log):
            logger.disabled = False

        self.recorder = RecordingHandler()
        root_logger = logging.getLogger()
        root_logger.addHandler(self.recorder)

    def tearDown(self):
        super(TornadoLoggingTestMixin, self).tearDown()
        logging.getLogger().removeHandler(self.recorder)


class TornadoLogFunctionTests(TornadoLoggingTestMixin,
                              testing.AsyncHTTPTestCase):

    def get_app(self):
        return web.Application(
            [web.url('/', SimpleHandler)],
            log_function=sprockets.logging.tornado_log_function)

    @property
    def access_record(self):
        for record, _ in self.recorder.emitted:
            if record.name == 'tornado.access':
                return record

    def test_that_redirect_logged_as_info(self):
        self.fetch('?status_code=303')
        self.assertEqual(self.access_record.levelno, logging.INFO)

    def test_that_client_error_logged_as_warning(self):
        self.fetch('?status_code=400')
        self.assertEqual(self.access_record.levelno, logging.WARNING)

    def test_that_exception_is_logged_as_error(self):
        self.fetch('/?runtime_error=something%20bad%20happened')
        self.assertEqual(self.access_record.levelno, logging.ERROR)

    def test_that_log_includes_correlation_id(self):
        self.fetch('/?runtime_error=something%20bad%20happened')
        self.assertIn('correlation_id', self.access_record.args)

    def test_that_log_includes_duration(self):
        self.fetch('/?runtime_error=something%20bad%20happened')
        self.assertIn('duration', self.access_record.args)

    def test_that_log_includes_headers(self):
        self.fetch('/?runtime_error=something%20bad%20happened')
        self.assertIn('headers', self.access_record.args)

    def test_that_log_includes_method(self):
        self.fetch('/?runtime_error=something%20bad%20happened')
        self.assertEqual(self.access_record.args['method'], 'GET')

    def test_that_log_includess_path(self):
        self.fetch('/?runtime_error=something%20bad%20happened')
        self.assertEqual(self.access_record.args['path'], '/')

    def test_that_log_includes_protocol(self):
        self.fetch('/?runtime_error=something%20bad%20happened')
        self.assertEqual(self.access_record.args['protocol'], 'http')

    def test_that_log_includes_query_arguments(self):
        self.fetch('/?runtime_error=something%20bad%20happened')
        self.assertEqual(self.access_record.args['query_args'],
                         {'runtime_error': ['something bad happened']})

    def test_that_log_includes_remote_ip(self):
        self.fetch('/?runtime_error=something%20bad%20happened')
        self.assertIn('remote_ip', self.access_record.args)

    def test_that_log_includes_status_code(self):
        self.fetch('/?runtime_error=something%20bad%20happened')
        self.assertEqual(self.access_record.args['status_code'], 500)

    def test_that_log_includes_environment(self):
        self.fetch('/?runtime_error=something%20bad%20happened')
        self.assertEqual(self.access_record.args['environment'],
                         os.environ['ENVIRONMENT'])

    def test_that_log_includes_correlation_id_from_header(self):
        cid = str(uuid.uuid4())
        self.fetch('/?runtime_error=something%20bad%20happened',
                   headers={'Correlation-ID': cid})
        self.assertEqual(self.access_record.args['correlation_id'], cid)


class JSONFormatterTests(TornadoLoggingTestMixin, testing.AsyncHTTPTestCase):

    def setUp(self):
        super(JSONFormatterTests, self).setUp()
        self.recorder.setFormatter(sprockets.logging.JSONRequestFormatter())

    def get_app(self):
        return web.Application(
            [web.url('/', SimpleHandler)],
            log_function=sprockets.logging.tornado_log_function)

    def get_log_line(self, log_name):
        for record, line in self.recorder.emitted:
            if record.name == log_name:
                return json.loads(line)

    def test_that_messages_are_json_encoded(self):
        self.fetch('/')
        for record, line in self.recorder.emitted:
            json.loads(line)

    def test_that_exception_has_traceback(self):
        self.fetch('/?runtime_error=foo')
        entry = self.get_log_line('tornado.application')
        self.assertIsNotNone(entry.get('traceback'))
        self.assertNotEqual(entry['traceback'], [])

    def test_that_successes_do_not_have_traceback(self):
        self.fetch('/')
        for record, line in self.recorder.emitted:
            entry = json.loads(line)
            self.assertNotIn('traceback', entry)


class ContextFilterTests(TornadoLoggingTestMixin, unittest.TestCase):

    def setUp(self):
        super(ContextFilterTests, self).setUp()
        self.logger = logging.getLogger('test-logger')
        self.recorder.setFormatter(
            logging.Formatter('%(message)s {CID %(correlation_id)s}'))
        self.recorder.addFilter(sprockets.logging.ContextFilter(
            properties=['correlation_id']))

    def test_that_property_is_set_to_none_by_filter_when_missing(self):
        self.logger.error('error message')
        _, line = self.recorder.emitted[0]
        self.assertEqual(line, 'error message {CID None}')

    def test_that_extras_property_is_used(self):
        self.logger.error('error message',
                          extra={'correlation_id': 'CORRELATION-ID'})
        _, line = self.recorder.emitted[0]
        self.assertEqual(line, 'error message {CID CORRELATION-ID}')

    def test_that_property_from_logging_adapter_works(self):
        cid = uuid.uuid4()
        logger = logging.LoggerAdapter(self.logger, {'correlation_id': cid})
        logger.error('error message')
        _, line = self.recorder.emitted[0]
        self.assertEqual(line, 'error message {CID %s}' % cid)
