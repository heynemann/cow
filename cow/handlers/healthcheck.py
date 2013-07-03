#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from tornado.web import RequestHandler, asynchronous
from tornado.gen import coroutine, Task


class HealthCheckHandler(RequestHandler):
    @asynchronous
    @coroutine
    def get(self):
        healthcheck_text = self.application.config.get('HEALTHCHECK_TEXT', 'WORKING')

        for plugin in self.application.plugins:
            result = yield Task(plugin.before_healthcheck, self.application)

            if not plugin.validate(result):
                self.set_status(500)
                self.write("HEALTCHECK FAILED")
                self.finish()
                return

            logging.info('[Healthcheck - %s] Got %s' % (
                plugin.__name__, result)
            )

        self.write(healthcheck_text)
        self.finish()
