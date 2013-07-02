#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import motor

from cow.plugins import BasePlugin


class MotorPlugin(BasePlugin):
    @classmethod
    def after_start(cls, application):
        host = application.config.get('MONGOHOST')
        port = application.config.get('MONGOPORT')
        db = application.config.get('MONGODATABASE')
        logging.info("Connecting to mongodb at %s:%d" % (host, port))
        application.mongoserver = motor.MotorClient(host, port).open_sync()
        application.mongo = application.mongoserver[db]

    @classmethod
    def before_end(cls, application):
        if hasattr(application, 'mongoserver'):
            logging.info("Disconnecting from mongodb...")
            application.mongoserver.disconnect()

    @classmethod
    def before_healthcheck(cls, application, callback):
        application.mongoserver.admin.command('ping', callback=callback)

    @classmethod
    def validate(cls, result, error, *args, **kw):
        if error is not None:
            logging.exception(error)
            return False

        return result.get('ok', 0) == 1.0
