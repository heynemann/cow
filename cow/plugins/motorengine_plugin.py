#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import motorengine
import motorengine.connection

from cow.plugins import BasePlugin


class MotorEnginePlugin(BasePlugin):
    @classmethod
    def after_start(cls, application, io_loop=None, *args, **kw):
        databases = application.config.get('MONGO_DATABASES')

        if not databases or not isinstance(databases, (dict,)):
            raise RuntimeError("MONGO_DATABASES configuration is required and should be a dictionary.")

        for key, value in databases.items():
            host = value['host']
            port = int(value['port'])
            db = value['database']
            username = value.get('username', None)
            password = value.get('password', None)

            conn_str = "mongodb://%s:%d/%s" % (host, port, db)

            if username is not None:
                if password is not None:
                    conn_str = "mongodb://%s:%s@%s:%d/%s" % (username, password, host, port, db)
                else:
                    conn_str = "mongodb://%s@%s:%d/%s" % (username, host, port, db)

            arguments = dict(
                host=conn_str,
                io_loop=io_loop
            )

            arguments['alias'] = key

            replica_set = arguments.get('replica_set', None)
            if replica_set is not None:
                arguments['replicaSet'] = replica_set

            logging.info("Connecting to mongodb at %s" % conn_str)
            motorengine.connect(db, **arguments)

    @classmethod
    def before_end(cls, application, *args, **kw):
        databases = application.config.get('MONGO_DATABASES')
        for key in databases.keys():
            logging.info("Disconnecting from mongodb[%s]..." % key)
            motorengine.disconnect(alias=key)

    @classmethod
    def before_healthcheck(cls, application, callback, *args, **kw):
        databases = application.config.get('MONGO_DATABASES')
        for key in databases.keys():
            conn = motorengine.connection.get_connection(alias=key).connection
            conn.admin.command('ping', callback=callback)

    @classmethod
    def validate(cls, result, *args, **kw):
        result, error = result.args

        if error is not None:
            logging.exception(error)
            return False

        return result.get('ok', 0) == 1.0
