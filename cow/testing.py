#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.testing import AsyncHTTPTestCase


class CowTestCase(AsyncHTTPTestCase):
    def tearDown(self):
        self.server.plugin_before_end(io_loop=self.io_loop)
        super(CowTestCase, self).tearDown()

    def get_server(self):
        raise NotImplementedError('You must implement the get_server method in your CowTestCase')

    def get_app(self):
        self.server = self.get_server()
        self.server.debug = True
        self.server.initialize_app()
        self.server.application.io_loop = self.io_loop

        self.server.plugin_after_start(io_loop=self.io_loop)
        return self.server.application
