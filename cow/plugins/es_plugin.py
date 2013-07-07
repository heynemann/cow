#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from json import loads

import tornadoes
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

from cow.plugins import BasePlugin


class ESPlugin(BasePlugin):
    @classmethod
    def after_start(cls, application, io_loop=None, *args, **kw):
        host = application.config.get('ELASTIC_SEARCH_HOST')
        port = application.config.get('ELASTIC_SEARCH_PORT')

        logging.info("Connecting to elastic search at %s:%d" % (host, port))

        application.elastic_search = tornadoes.ESConnection(host, port, io_loop=io_loop)
        application.elastic_search_host = host
        application.elastic_search_port = port

    @classmethod
    def before_end(cls, application, *args, **kw):
        if hasattr(application, 'elastic_search'):
            logging.info("Disconnecting from elastic search...")
            del application.elastic_search

    @classmethod
    def before_healthcheck(cls, application, callback, *args, **kw):
        url = "http://%s:%d/_cluster/health?pretty=true" % (application.elastic_search_host, application.elastic_search_port)
        client = AsyncHTTPClient(application.io_loop)
        request_http = HTTPRequest(url, method="GET")
        client.fetch(request=request_http, callback=callback)

    @classmethod
    def validate(cls, result, *args, **kw):
        if result.code != 200:
            logging.error("Elastic Search healthcheck failed with %s" % result.body)
            return False

        result = loads(result.body)
        return result['status'] in ['green', 'yellow']
