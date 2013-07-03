#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from tornadoredis import Client

from cow.plugins import BasePlugin


class RedisPlugin(BasePlugin):
    @classmethod
    def after_start(cls, application, io_loop=None, *args, **kw):
        host = application.config.get('REDISHOST')
        port = application.config.get('REDISPORT')
        db = int(application.config.get('REDISDB', 0))
        password = application.config.get('REDISPASS', None)

        logging.info("Connecting to redis at %s:%d" % (host, port))
        arguments = dict(
            host=host,
            port=port,
            selected_db=db
        )

        if io_loop is not None:
            arguments['io_loop'] = io_loop

        if password is not None:
            arguments['password'] = password

        application.redis = Client(**arguments)
        application.redis.connect()

    @classmethod
    def before_end(cls, application, *args, **kw):
        if hasattr(application, 'redis'):
            logging.info("Disconnecting from redis...")
            application.redis.disconnect()

    @classmethod
    def before_healthcheck(cls, application, callback, *args, **kw):
        application.redis.ping(callback=callback)

    @classmethod
    def validate(cls, result, *args, **kw):
        if not result:
            logging.exception("Could not connect to redis")
            return False

        return bool(result)
