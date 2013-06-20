#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.testing import AsyncHTTPTestCase
from preggy import expect

from tests.sandbox.server import SandboxServer
from tests.sandbox.config import Config


class TestHealthCheck(AsyncHTTPTestCase):
    def get_app(self):
        return SandboxServer().application

    def test_healthcheck(self):
        response = self.fetch('/healthcheck')
        expect(response.code).to_equal(200)
        expect(response.body).to_be_like('WORKING')


class TestHealthCheckWithCustomString(AsyncHTTPTestCase):
    def get_app(self):
        cfg = Config(HEALTHCHECK_TEXT='SOMETHING ELSE')
        return SandboxServer(config=cfg).application

    def test_healthcheck(self):
        response = self.fetch('/healthcheck')
        expect(response.code).to_equal(200)
        expect(response.body).to_be_like('SOMETHING ELSE')
