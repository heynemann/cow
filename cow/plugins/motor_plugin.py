#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import motor

from cow.plugins import BasePlugin


class MotorPlugin(BasePlugin):
    @classmethod
    def after_start(cls, application, io_loop=None, *args, **kw):
        host = application.config.get('MONGOHOST')
        port = application.config.get('MONGOPORT')
        db = application.config.get('MONGODATABASE')

        if not db:
            raise RuntimeError("MONGODATABASE configuration is required.")

        logging.info("Connecting to mongodb at %s:%d" % (host, port))
        application.mongoserver = motor.MotorClient(host, port, io_loop=io_loop).open_sync()
        application.mongo = application.mongoserver[db]

    @classmethod
    def before_end(cls, application, *args, **kw):
        if hasattr(application, 'mongoserver'):
            logging.info("Disconnecting from mongodb...")
            application.mongoserver.disconnect()

    @classmethod
    def before_healthcheck(cls, application, callback, *args, **kw):
        application.mongoserver.admin.command('ping', callback=callback)

    @classmethod
    def validate(cls, result, *args, **kw):
        result, error = result.args

        if error is not None:
            logging.exception(error)
            return False

        return result.get('ok', 0) == 1.0
