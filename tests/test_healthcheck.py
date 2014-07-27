#!/usr/bin/python
# -*- coding: utf-8 -*-

from preggy import expect

from tests import TestCase


class TestHealthCheck(TestCase):

    def test_healthcheck(self):
        response = self.fetch('/healthcheck')
        expect(response.code).to_equal(200)
        expect(response.body).to_be_like('WORKING')


class TestHealthCheckWithCustomString(TestCase):
    def get_config(self):
        cfg = super(TestHealthCheckWithCustomString, self).get_config()
        cfg['HEALTHCHECK_TEXT'] = 'SOMETHING ELSE'
        return cfg

    def test_healthcheck(self):
        response = self.fetch('/healthcheck')
        expect(response.code).to_equal(200)
        expect(response.body).to_be_like('SOMETHING ELSE')
