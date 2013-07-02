#!/usr/bin/env python
# -*- coding: utf-8 -*-

import motor

from cow.plugins import BasePlugin


class MotorPlugin(BasePlugin):
    @classmethod
    def after_start(cls, server):
        host = server.application.config.get('MONGOHOST')
        port = server.application.config.get('MONGOPORT')
        server.mongo = motor.MotorClient(host, port).open_sync()

    @classmethod
    def before_end(cls, server):
        if hasattr(server, 'mongo'):
            server.mongo.disconnect()
