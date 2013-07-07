#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from toredis import Client

from cow.plugins import BasePlugin


class RedisPlugin(BasePlugin):
    @classmethod
    def has_connected(cls, application):
        def handle(*args, **kw):
            password = application.config.get('REDISPASS', None)
            if password:
                application.redis.auth(password, callback=cls.handle_authenticated(application))
            else:
                cls.handle_authenticated(application)()
        return handle

    @classmethod
    def handle_authenticated(cls, application):
        def handle(*args, **kw):
            application.redis.authenticated = True

        return handle

    @classmethod
    def after_start(cls, application, io_loop=None, *args, **kw):
        host = application.config.get('REDISHOST')
        port = application.config.get('REDISPORT')

        logging.info("Connecting to redis at %s:%d" % (host, port))

        application.redis = Client(io_loop=io_loop)
        application.redis.authenticated = False
        application.redis.connect(host, port, callback=cls.has_connected(application))

    @classmethod
    def before_end(cls, application, *args, **kw):
        if hasattr(application, 'redis'):
            logging.info("Disconnecting from redis...")
            del application.redis

    @classmethod
    def before_healthcheck(cls, application, callback, *args, **kw):
        application.redis.ping(callback=callback)

    @classmethod
    def validate(cls, result, *args, **kw):
        if not result:
            logging.exception("Could not connect to redis")
            return False

        return result == "PONG"
