#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import motor

from cow.plugins import BasePlugin


class MotorPlugin(BasePlugin):
    @classmethod
    def after_start(cls, server):
        host = server.application.config.get('MONGOHOST')
        port = server.application.config.get('MONGOPORT')
        logging.info("Connecting to mongodb at %s:%d" % (host, port))
        server.mongo = motor.MotorClient(host, port).open_sync()

    @classmethod
    def before_end(cls, server):
        if hasattr(server, 'mongo'):
            logging.info("Disconnecting from mongodb...")
            server.mongo.disconnect()
