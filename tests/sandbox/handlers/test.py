#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler


class TestHandler(RequestHandler):
    def get(self):
        self.write(self.application.config.TESTCONF)
