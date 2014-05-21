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
        user = application.config.get('MONGOUSER')
        password = application.config.get('MONGOPASS')

        if not db:
            raise RuntimeError("MONGODATABASE configuration is required.")

        conn_str = "%s:%d/%s" % (host, port, db)
        user_str = ""

        if user is not None:
            user_str = user
            if password is not None:
                user_str = "%s:%s" % (user, password)

        conn = "mongodb://%s%s" % (user_str, conn_str)

        logging.info("Connecting to mongodb at %s" % (conn_str))
        application.mongoserver = motor.MotorClient(conn, io_loop=io_loop)
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
