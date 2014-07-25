#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from tornado.httpclient import AsyncHTTPClient
import gandalf.tornado_cli as client

from cow.plugins import BasePlugin


class GandalfPlugin(BasePlugin):
    @classmethod
    def after_start(cls, application, io_loop=None, *args, **kw):
        host = application.config.get('GANDALF_HOST')
        port = application.config.get('GANDALF_PORT')

        logging.info("Connecting to gandalf at %s:%d" % (host, port))

        http_client = AsyncHTTPClient(io_loop or application.io_loop)
        application.gandalf = client(host, port, http_client.fetch)

    @classmethod
    def before_end(cls, application, *args, **kw):
        if hasattr(application, 'elastic_search'):
            logging.info("Disconnecting from gandalf...")
            del application.gandalf

    @classmethod
    def before_healthcheck(cls, application, callback, *args, **kw):
        application.gandalf.healthcheck(callback=callback)

    @classmethod
    def validate(cls, result, *args, **kw):
        if result:
            logging.error("Gandalf healthcheck failed with %s" % result.body)
            return False

        return True

    @classmethod
    def define_configurations(cls, config):
        config.define('GANDALF_HOST', 'localhost', 'Host for the gandalf server.', 'Gandalf')
        config.define('GANDALF_PORT', 8001, 'Port for the gandalf server.', 'Gandalf')
