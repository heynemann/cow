#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from tornado.httpclient import AsyncHTTPClient
from tornado.concurrent import is_future
import tornado.gen as gen
import gandalf.tornado_cli as client

from cow.plugins import BasePlugin


class GandalfPlugin(BasePlugin):
    @classmethod
    def after_start(cls, application, io_loop=None, *args, **kw):
        host = application.config.get('GANDALF_HOST')
        port = application.config.get('GANDALF_PORT')

        logging.info("Connecting to gandalf at %s:%d" % (host, port))

        http_client = AsyncHTTPClient(io_loop or application.io_loop)
        application.gandalf = client.AsyncTornadoGandalfClient(host, port, http_client.fetch)

    @classmethod
    def before_end(cls, application, *args, **kw):
        if hasattr(application, 'elastic_search'):
            logging.info("Disconnecting from gandalf...")
            del application.gandalf

    @classmethod
    @gen.coroutine
    def before_healthcheck(cls, application, *args, **kw):
        result = application.gandalf.healthcheck()
        if is_future(result):
            result = yield result
        raise gen.Return(result)

    @classmethod
    def validate(cls, result, *args, **kw):
        if not result:
            logging.error("Gandalf healthcheck failed...")
            return False

        return True

    @classmethod
    def define_configurations(cls, config):
        config.define('GANDALF_HOST', 'localhost', 'Host for the gandalf server.', 'Gandalf')
        config.define('GANDALF_PORT', 8001, 'Port for the gandalf server.', 'Gandalf')
