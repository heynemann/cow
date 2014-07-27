#!/usr/bin/python
# -*- coding: utf-8 -*-

from preggy import expect

from tests import TestCase


class TestSandboxServer(TestCase):
    def test_homepage(self):
        response = self.fetch('/')
        expect(response.code).to_equal(200)
        expect(response.body).to_be_like('test-configuration')

    def test_healthcheck(self):
        response = self.fetch('/healthcheck/')
        expect(response.code).to_equal(200)
        expect(response.body).to_be_like('WORKING')
