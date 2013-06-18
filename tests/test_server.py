#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.testing import AsyncHTTPTestCase
from preggy import expect

from tests.sandbox.server import SandboxServer


class TestSandboxServer(AsyncHTTPTestCase):
    def get_app(self):
        return SandboxServer().application

    def test_homepage(self):
        response = self.fetch('/')
        expect(response.code).to_equal(200)
        expect(response.body).to_be_like('test-configuration')
