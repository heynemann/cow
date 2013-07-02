#!/usr/bin/python
# -*- coding: utf-8 -*-

from cow.testing import CowTestCase
from preggy import expect

from tests.sandbox.server import SandboxServer
from tests.sandbox.config import Config


class TestHealthCheck(CowTestCase):
    def get_server(self):
        return SandboxServer()

    def test_healthcheck(self):
        response = self.fetch('/healthcheck')
        expect(response.code).to_equal(200)
        expect(response.body).to_be_like('WORKING')


class TestHealthCheckWithCustomString(CowTestCase):
    def get_server(self):
        cfg = Config(HEALTHCHECK_TEXT='SOMETHING ELSE')
        return SandboxServer(config=cfg)

    def test_healthcheck(self):
        response = self.fetch('/healthcheck')
        expect(response.code).to_equal(200)
        expect(response.body).to_be_like('SOMETHING ELSE')
