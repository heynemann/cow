#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.testing import AsyncHTTPTestCase
from preggy import expect

from tests.sandbox.server import SandboxServer


class TestHealthCheck(AsyncHTTPTestCase):
    def get_app(self):
        return SandboxServer().application

    def test_healthcheck(self):
        response = self.fetch('/healthcheck')
        expect(response.code).to_equal(200)
        expect(response.body).to_be_like('WORKING')
