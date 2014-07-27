#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from cow.plugins.sqlalchemy_plugin import SQLAlchemyMixin


class TestHandler(RequestHandler, SQLAlchemyMixin):
    def get(self):
        self.write(self.application.config.TESTCONF)
