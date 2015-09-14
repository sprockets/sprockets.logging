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
