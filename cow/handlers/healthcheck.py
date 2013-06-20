#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler


class HealthCheckHandler(RequestHandler):
    def get(self):
        healthcheck_text = self.application.config.get('HEALTHCHECK_TEXT', 'WORKING')
        self.write(healthcheck_text)
