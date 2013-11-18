#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import redis

from cow.plugins import BasePlugin


class RedisPlugin(BasePlugin):
    @classmethod
    def after_start(cls, application, io_loop=None, *args, **kw):
        host = application.config.get('REDISHOST')
        port = application.config.get('REDISPORT')

        logging.info("Connecting to redis at %s:%d" % (host, port))

        application.redis = redis.StrictRedis(host=host, port=int(port), db=0)
        application.redis.authenticated = False

        password = application.config.get('REDISPASS', None)
        if password:
            application.redis.auth(password)
            application.redis.authenticated = True

    @classmethod
    def before_end(cls, application, *args, **kw):
        if hasattr(application, 'redis'):
            logging.info("Disconnecting from redis...")
            del application.redis

    @classmethod
    def before_healthcheck(cls, application, callback, *args, **kw):
        callback(application.redis.ping())

    @classmethod
    def validate(cls, result, *args, **kw):
        if not result:
            logging.exception("Could not connect to redis")
            return False

        return result == "PONG"
